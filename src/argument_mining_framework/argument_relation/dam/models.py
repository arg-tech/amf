
import json
import os
import sys
import os
import json
from transformers import AutoTokenizer, AutoModel, BertForTokenClassification, BartForSequenceClassification, BertTokenizer, BartTokenizer
from sentence_transformers import SentenceTransformer
from transformers import pipeline
#sys.path.append('/Users/debelagemechu/projects/amf/dam')  # Add the parent directory of 'src' to the Python path
#from decompose.subject_verb_object_extract import findSVOs, nlp






class ModelLoader:
    def __init__(self, config_file='dam/config/config.json'):
        script_directory = os.path.dirname(os.path.abspath(__file__))       
        parent_directory = os.path.dirname(script_directory)
        config_directory = os.path.join(parent_directory, 'config')
        config_file_path = os.path.join(parent_directory, config_file)
        self.config_file = config_file_path
        self.load_config()
        self.load_models()

    def load_config(self):
        with open(self.config_file, 'r') as f:
            self.config = json.load(f)

    def load_models(self):
        # Load SentenceTransformer model
        self.s_bert_model = SentenceTransformer(self.config['sentence_transformers_model'])

        # Load tokenizer and model for sentence BERT
        self.tokenizer = AutoTokenizer.from_pretrained(self.config['sentence_bert_tokenizer'])
        self.model = AutoModel.from_pretrained(self.config['sentence_bert_model'])
        #
        # Load tokenizer for token classification
        self.token_clsification_tokenizer = BertTokenizer.from_pretrained(self.config['bert_tokenizer'], do_lower_case=False)

        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.realpath(__file__))


        self.decompositional_model = BertForTokenClassification.from_pretrained(self.config['model_directory'])
        # Construct the relative path to the model directory
        '''
        model_dir = os.path.join(current_dir, self.config['model_directory'], 'model_token_clasiffier')
        # Check if the model directory exists
        if os.path.exists(model_dir):
            # Load the token classification model
            self.decompositional_model = BertForTokenClassification.from_pretrained(model_dir)
            print("Model loaded")
        else:
            print("Model directory is not found:", model_dir)
        '''

        # Load tokenizer and model for entailment
        self.tokenizer_enatilement = BartTokenizer.from_pretrained(self.config['bart_tokenizer'])
        self.model_enatilement = BartForSequenceClassification.from_pretrained(self.config['bart_model'])

        # Load sentiment classifier pipeline
        self.sentiment_classifier = pipeline('sentiment-analysis')

if __name__ == "__main__":
    model_loader = ModelLoader()
