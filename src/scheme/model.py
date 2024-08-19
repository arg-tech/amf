from transformers import AutoTokenizer, pipeline

class Loader:
    def __init__(self, model_name):
        self.model_name = model_name

    def load_model(self):
        # Load the model and tokenizer into a pipeline
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        classifier = pipeline("text-classification", model=self.model_name, tokenizer=tokenizer)
        return classifier, tokenizer

