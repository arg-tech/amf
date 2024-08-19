from ..argument_relation.model import Loader

class SchemeClassifier:
    def __init__(self):
        self.tokenizer, self.model = Loader.load_model("raruidol/SchemeClassifier3-ENG")
    
    def classify(self, text):
        inputs = self.tokenizer(text, return_tensors="pt")
        outputs = self.model(**inputs)
        predictions = outputs.logits.argmax(dim=-1)
        return predictions.item()
