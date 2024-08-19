from ..argument_relation.model import Loader

class HypothesisClassifier:
    def __init__(self):
        self.tokenizer, self.model = Loader.load_model("raruidol/HypothesisMining-EN-Loc")
    
    def classify(self, text):
        inputs = self.tokenizer(text, return_tensors="pt")
        outputs = self.model(**inputs)
        predictions = outputs.logits.argmax(dim=-1)
        return predictions.item()
