


# amf/__init__.py
from amf.src.argument_relation.predictor import ArgumentRelationPredictor
from amf.src.scheme.predictor import SchemePredictor
from amf.src.hypothesis.predictor import HypothesisPredictor

# Create simplified access to the predictor classes
def argument_relation(model_type: str, variant: str):
    return ArgumentRelationPredictor(model_type, variant)

def scheme(model_type: str, variant: str):
    return SchemePredictor(model_type, variant)

def hypothesis(model_type: str, variant: str):
    return HypothesisPredictor(model_type, variant)

__all__ = ['argument_relation', 'scheme', 'hypothesis']
