import torch
from torch.nn import functional as F
import numpy as np
import pandas as pd
from scipy.special import softmax
import spacy
import sys
#sys.path.append('amf/src/argument_mining_framework/argument_relation/dam')  # Add the parent directory of 'src' to the Python path


from argument_mining_framework.argument_relation.dam.models import ModelLoader
import os
modelloader = ModelLoader()

nlp = spacy.load("en_core_web_lg")

class TokenClassificationModel:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.MAX_LEN = 30
        self.decompositional_model = modelloader.decompositional_model
        self.decompositional_model.to(self.device)
        self.decompositional_model.eval()
        abs_path = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.join(abs_path, "../config/spacy_tag_dep.csv")
        self.df  = pd.read_csv(file_path, encoding="utf-8")
        self.list_tags = self.df.Label.values
        self.tokenizer = self.add_spacy_tags_ber_tokenizer(modelloader.token_clsification_tokenizer, self.list_tags)
        self.tag2idx = {'O\n': 0, 'B-OC\n': 1, 'I-null\n': 2, 'B-C\n': 3, 'B-null\n': 4, 'I-OC\n': 5, 'B-OA\n': 6, 'B-A\n': 7, 'I-OA\n': 8, 'I-A\n': 9, 'I-C\n': 10, 'PAD': 11}
        self.tag2name = {self.tag2idx[key]: key for key in self.tag2idx.keys()}

    def add_spacy_tags_ber_tokenizer(self, tokenizer, list_spacy_tags):
        pos_tags = ["ADJ", "ADP", "ADV", "AUX", "CONJ", "CCONJ", "DET", "INTJ", "NOUN", "NUM", "PART", "PRON", "PROPN", 
                    "PUNCT", "SCONJ", "SYM", "VERB", "X", "SPACE"]
        for tag in list_spacy_tags:
            for pos in pos_tags:
                tokenizer.add_tokens([tag.lower() + pos.lower()])
        return tokenizer

    def pad_sequences_post(self, seq, maxlen, dtype='long'):
        output = []
        for s in seq:
            s = self.tokenizer.convert_tokens_to_ids(s)
            if len(s) < maxlen:
                output.append(np.concatenate([s, np.zeros(maxlen - len(s))]))
            else:
                output.append(s[:maxlen])
        return np.array(output, dtype=dtype)

    def inference(self, input_text_dependency_format, raw_input_text):
        input_text_dependency_format = input_text_dependency_format.lower()
        tokenized_texts = []
        temp_token_dependency_format = []
        temp_token_raw_text = []
        temp_token_dependency_format.append('[CLS]')
        temp_token_raw_text.append('[CLS]')
        token_list_dependency_format = self.tokenizer.tokenize(input_text_dependency_format)
        token_list_raw_text = self.tokenizer.tokenize(raw_input_text)

        for m, token in enumerate(token_list_dependency_format):
            temp_token_dependency_format.append(token)
        for m, token in enumerate(token_list_raw_text):
            temp_token_raw_text.append(token)

        if len(temp_token_dependency_format) > self.MAX_LEN - 1:
            temp_token_dependency_format = temp_token_dependency_format[:self.MAX_LEN - 1]
        if len(temp_token_raw_text) > self.MAX_LEN - 1:
            temp_token_raw_text = temp_token_raw_text[:self.MAX_LEN - 1]

        temp_token_dependency_format.append('[SEP]')
        temp_token_raw_text.append('[SEP]')

        tokenized_texts.append(temp_token_dependency_format)

        input_ids = self.pad_sequences_post(tokenized_texts, maxlen=self.MAX_LEN, dtype="int64")
        attention_masks = [[int(i > 0) for i in ii] for ii in input_ids]

        segment_ids = [[0] * len(input_id) for input_id in input_ids]

        input_ids = torch.tensor(input_ids)
        attention_masks = torch.tensor(attention_masks)
        segment_ids = torch.tensor(segment_ids)

        with torch.no_grad():
            outputs = self.decompositional_model(input_ids.to(self.device), token_type_ids=None, attention_mask=None,)
            logits = outputs[0]

        predict_results = logits.detach().cpu().numpy()
        result_arrays_soft = softmax(predict_results[0])
        result_array = result_arrays_soft

        result_list = np.argmax(result_array, axis=-1)

        target_concept = []
        aspect = []
        target_concept_opinion = []

        for i, mark in enumerate(attention_masks[0]):
            if mark > 0:
                token = temp_token_dependency_format[i]
                tag = self.tag2name[result_list[i]]

                if str(tag).strip() == 'B-A' or str(tag).strip() == 'I-A':
                    aspect.append(token)
                elif str(tag).strip() == 'B-C' or str(tag).strip() == 'I-C':
                    target_concept.append(token)
                elif str(tag).strip() == 'B-OC' or str(tag).strip() == 'I-OC' or str(tag).strip() == 'B-OA' or str(tag).strip() == 'I-OA':
                    target_concept_opinion.append(token)

        return ' '.join(target_concept), ' '.join(aspect), ' '.join(target_concept_opinion)

    def dependency_tag(self, sentence):
        tags = []
        dct_index_tag_token = {}
        doc = nlp(sentence)
        for token in doc:
            tags.append(str(token.dep_ + token.pos_).lower())
            dct_index_tag_token[token.text] = str(token.dep_ + token.pos_).lower()
        return tags, dct_index_tag_token

    def post_process(self, texts_list):
        target_concept, aspects, opinions = [], [], []
        for texts in texts_list:
            text_sentences = nlp(texts)
            for sentence in text_sentences.sents:
                text = sentence.text.strip()
                if text != "":
                    raw_text = text
                    tokens, dct_index_tag_token = self.dependency_tag(text)
                    dependency_text = ' '.join(tokens)
                    tcs, asps, ops = self.inference(dependency_text, raw_text)
                    tcs = tcs.replace(" _ ", "_").replace("[CLS]", "").replace("[SEP]", "").replace(" ##", "")
                    asps = asps.replace(" _ ", "_").replace("[CLS]", "").replace("[SEP]", "").replace(" ##", "")
                    ops = ops.replace(" _ ", "_").replace("[CLS]", "").replace("[SEP]", "").replace(" ##", "")

                    tcs_f, asps_f, ops_f = [], [], []

                    tcs_all = tcs.split(" ")
                    tcs_n = [tc.replace(" ", "").strip() for tc in tcs_all if tc.strip() != ""]

                    for key, value in dct_index_tag_token.items():
                        for tc in tcs_n:
                            if value == tc and key not in tcs_f:
                                tag_set = ['NN', 'NNS', 'NNP']
                                key = self.filter_tag(key, tag_set)
                                tcs_f.append(key)

                    asps_all = asps.split(" ")
                    asps_n = [asp.strip() for asp in asps_all]

                    asps_n_extended = []
                    for asp_n in asps_n:
                        splited_by_space = asp_n.split(" ")
                        asps_n_extended.extend(concepts_element for concepts_element in splited_by_space)

                    for key, value in dct_index_tag_token.items():
                        for asp in asps_n_extended:
                            if value == asp and key not in asps_f:
                                tag_set = ['NN', 'NNS,NNP']
                                key = self.filter_tag(key, tag_set)
                                asps_f.append(key)

                    ops_all = ops.split(" ")
                    ops_n = [op.strip() for op in ops_all]
                    for key, value in dct_index_tag_token.items():
                        for op in ops_n:
                            if value == op and key not in ops_f:
                                ops_f.append(key)
                    target_concept.append(' '.join(tcs_f))
                    aspects.append(' '.join(asps_f))
                    opinions.append(' '.join(ops_f))
        return (target_concept, aspects, opinions)

    def filter_tag(self, text, tag_set):
        filtered_text = ""
        doc = nlp(text)        
        for token in doc:
            if token.tag_ in tag_set and token.tag_ not in ['PRP']:
               filtered_text += " " + token.text
        filtered_text = filtered_text.strip()
        return filtered_text
'''
# Example usage:
clasification_output = TokenClassificationModel()
texts_list= ["there would be no non-tariff barriers with the deal done with the EU"]
texts_list = ["there are lots of non-tariff barriers with the deal done with the EU"]
components = clasification_output.post_process(texts_list)
print(components)
'''
