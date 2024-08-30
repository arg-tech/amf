
from argument_mining_framework.argument_relation.dam.decompose.get_components import FunctionalComponentsExtractor
from argument_mining_framework.argument_relation.dam.features.sentiment import get_sentiment
from argument_mining_framework.argument_relation.dam.features.similarity import get_sim,sim_feature,get_sim_dam1_2
import logging
logging.basicConfig(level=logging.INFO)


class Dam2ArgumentRelationAnalyzer:
    def __init__(self):
        pass

    @classmethod
    def get_argument_relation(cls, p1p2):
        text1, text2 = p1p2
        functional_components_p1, functional_components_p2 = cls._get_functional_components(text1, text2)
        sentiment = cls._get_sentiment(text1, text2)
        arg_rel1 = cls._get_arg_relation(functional_components_p1, functional_components_p2, sentiment)
        arg_rel2 = cls._get_arg_relation(functional_components_p2, functional_components_p1, sentiment)
        return cls._final_result(arg_rel2, arg_rel1)

    @classmethod
    def _get_arg_relation(cls, components1, components2, sentiment):
        similarity, antonymy = cls._get_sim(components1, components2)
        if not antonymy:
            antonymy = [0]
        return cls._sim_entail_argrel(similarity, sentiment, antonymy)
    @staticmethod
    def _sim_entail_argrel(similarity, entailemt, antonymy):
        logging.info(f"Antonym entailemt and  similarity:  {antonymy}, {entailemt}, {similarity}")

        if sim_feature(similarity) and entailemt and antonymy[0] == 0:
            return "Inference"
        elif sim_feature(similarity) and not entailemt:
            return "Attack"
        elif antonymy[0] == 1 and (not entailemt or entailemt):
            return "Attack"
        else:
            return "None"
        
    @staticmethod
    def _final_result(arg_rel2, arg_rel1):
        if arg_rel2 == "Attack" or arg_rel1 == "Attack":
            return "CA"
        elif arg_rel2 == "Inference" or arg_rel1 == "Inference":
            return "RA"
        else:
            return "None"

    @staticmethod
    def _get_functional_components(text1, text2):
        extractor = FunctionalComponentsExtractor()
        return extractor.get_rule_based_functional_components((text1, text2))

    @staticmethod
    def _get_sentiment(text1, text2):
        return get_sentiment(text1, text2)

    @staticmethod
    def _get_sim(components1, components2):
        return get_sim_dam1_2(components1, components2)
    





