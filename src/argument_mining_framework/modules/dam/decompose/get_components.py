import sys
#sys.path.append('/Users/debelagemechu/projects/amf/dam')  # Add the parent directory of 'src' to the Python path

from nltk.corpus import stopwords

from .token_clasifier_inference import TokenClassificationModel
from .svo_patterns import get_dependecy_parsing_patterns, get_components_svo
from .subject_verb_object_extract import findSVOs, nlp

class FunctionalComponentsExtractor:
    def __init__(self):
        self.token_classifier = TokenClassificationModel()

    def get_rule_based_functional_components(self, pair_of_propositions):
        text1, text2 = pair_of_propositions
        doc1 = nlp(text1)
        doc2 = nlp(text2)
        text1_components = self._get_components(doc1)
        text2_components = self._get_components(doc2)
        clean_text1_components = self._remove_stop_words(text1_components)
        clean_text2_components = self._remove_stop_words(text2_components)
        return clean_text1_components, clean_text2_components

    def get_model_based_functional_components(self, pair_of_propositions):
        text1, text2 = pair_of_propositions
        d_tc_c, d_asp_c, _ = self.token_classifier.post_process([text1])
        svo_tc_c, svo_asp_c, _ = get_components_svo(text1)
        merged_tc_c = list(set(svo_tc_c) | set([" ".join(d_tc_c)]))
        merged_asp_c = list(set(svo_asp_c) | set([" ".join(d_asp_c)]))

        d_tc_p, d_asp_p, _ = self.token_classifier.post_process([text2])
        svo_tc_p, svo_asp_p, _ = get_components_svo(text2)
        merged_tc_p = list(set(svo_tc_p) | set([" ".join(d_tc_p)]))
        merged_asp_p = list(set(svo_asp_p) | set([" ".join(d_asp_p)]))

        merged_tc_c_clean = self._clean_components(merged_tc_c)
        
        merged_asp_c_clean = self._clean_components(merged_asp_c)
        merged_tc_p_clean = self._clean_components(merged_tc_p)
        merged_asp_p_clean = self._clean_components(merged_asp_p)

        # Handle unrecognized components using patterns
        (merged_tc_c_clean, merged_asp_c_clean,
         merged_tc_p_clean, merged_asp_p_clean) = self._handle_unrecognized_components(
            text1, text2, merged_tc_c_clean, merged_asp_c_clean, merged_tc_p_clean, merged_asp_p_clean)

        return merged_tc_c_clean, merged_tc_p_clean, merged_asp_c_clean, merged_asp_p_clean

    def _get_components(self, doc):
        svos = findSVOs(doc)
        more_elements = get_dependecy_parsing_patterns(doc)
        comp = [list(elem) for elem in svos]
        more_elements = [list(elem) for elem in more_elements]
        comp += more_elements
        return comp
    def remove_repeatyed(self,input_list):
        cleaned_list = []
        for item in input_list:
            if not any(item in other_item and item != other_item for other_item in input_list):
                cleaned_list.append(item)
        return cleaned_list

    def _remove_stop_words(self, components):
        cleaned_components = []
        for ll in components:
            wrd_lst = []
            for phrase in ll:
                phrase_wrd = ""
                tokens = phrase.split()
                for word in tokens:
                    if word not in stopwords.words('english') and word:
                        phrase_wrd += " " + word.strip()
                if phrase_wrd:
                    wrd_lst.append(phrase_wrd.strip())
            cleaned_components.append(wrd_lst)
        return cleaned_components
    
    def dependency_tag(self, sentence):
        tags = []
        dct_index_tag_token = {}
        doc = nlp(sentence)
        for token in doc:
            tags.append(str((token.dep_ , token.pos_)))
            dct_index_tag_token[token.text] = (str(token.dep_) ,str(token.pos_))
        return dct_index_tag_token

    def _clean_components(self, components):
        cleaned_components = []
        for comp in components:
            cleaned_tokens = []
            #token_tag_dct = pos_tag([comp])
            tags_toks = self.dependency_tag(comp)
            for tok, tag in tags_toks.items():
                if tag[1] in ['NNP', 'NN', 'VBP', 'NNS', 'NOUN','NOUNS']:
                    cleaned_tokens.append(tok)
            if cleaned_tokens:
                cleaned_components.append(" ".join(cleaned_tokens))
        return self.remove_repeatyed(cleaned_components)

    def _handle_unrecognized_components(self, text1, text2, merged_tc_c_clean, merged_asp_c_clean, merged_tc_p_clean, merged_asp_p_clean):
        if len(merged_tc_c_clean) == 0 or len(merged_asp_c_clean) == 0:
            doc = nlp(text1)
            c_patterns_tc, c_pattern_asp, _ = get_dependecy_parsing_patterns(doc)
            if len(merged_tc_c_clean) == 0:
                merged_tc_c_clean = c_patterns_tc
            if len(merged_asp_c_clean) == 0:
                merged_asp_c_clean = c_pattern_asp
        if len(merged_tc_p_clean) == 0 or len(merged_asp_p_clean) == 0:
            doc = nlp(text2)
            p_patterns_tc, p_pattern_asp, _ = get_dependecy_parsing_patterns(doc)
            if len(merged_tc_p_clean) == 0:
                merged_tc_p_clean = p_patterns_tc
            if len(merged_asp_p_clean) == 0:
                merged_asp_p_clean = p_pattern_asp

        return merged_tc_c_clean, merged_asp_c_clean, merged_tc_p_clean, merged_asp_p_clean
