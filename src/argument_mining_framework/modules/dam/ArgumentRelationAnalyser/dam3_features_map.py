import sys
#sys.path.append('/Users/debelagemechu/projects/amf/dam')  # Add the parent directory of 'src' to the Python path

import sys
from argument_mining_framework.argument_relation.dam.features.similarity import get_sim, get_anotnyms_dam3,sim_feature
from argument_mining_framework.argument_relation.dam.features.entailment import get_entailement
from argument_mining_framework.argument_relation.dam.decompose.get_components import FunctionalComponentsExtractor

class Dam3ArgumentRelationAnalyzer:
    THRESHOLD_SIMILARITY = 75
    THRESHOLD_ANTONYMS = 55

    @staticmethod
    def get_argument_components(pair_of_propositions):
        text1, text2 = pair_of_propositions
        merged_tc_c, merged_tc_p, merged_asp_c, merged_asp_p = \
            Dam3ArgumentRelationAnalyzer._get_functional_components_dam3(pair_of_propositions)
        return merged_tc_c, merged_tc_p, merged_asp_c, merged_asp_p

    @staticmethod
    def get_argument_relation(pair_of_propositions):
        text1, text2 = pair_of_propositions
        merged_tc_c, merged_tc_p, merged_asp_c, merged_asp_p = \
            Dam3ArgumentRelationAnalyzer._get_functional_components_dam3(pair_of_propositions)

        sim_tc_conclusion_premise = Dam3ArgumentRelationAnalyzer._calculate_similarity(
            merged_tc_c, merged_tc_p, get_sim
        )
        sim_tc_conclusion_asp_premise = Dam3ArgumentRelationAnalyzer._calculate_similarity(
            merged_tc_p, merged_asp_c, get_sim
        )
        sim_asp_conclusion_tc_premise = Dam3ArgumentRelationAnalyzer._calculate_similarity(
            merged_tc_c, merged_asp_p, get_sim
        )
        sim_asp_conclusion_asp_premise = Dam3ArgumentRelationAnalyzer._calculate_similarity(
            merged_asp_p, merged_asp_c, get_sim
        )

        antonyms_tc_c = Dam3ArgumentRelationAnalyzer._get_antonyms(merged_tc_c)
        antonyms_tc_p = Dam3ArgumentRelationAnalyzer._get_antonyms(merged_tc_p)
        antonyms_asp_c = Dam3ArgumentRelationAnalyzer._get_antonyms(merged_asp_c)
        antonyms_asp_p = Dam3ArgumentRelationAnalyzer._get_antonyms(merged_asp_p)

        entailemt = Dam3ArgumentRelationAnalyzer._get_entailement(text1, text2)

        print("entailemt", entailemt, "antonymys_asp_p", antonyms_asp_p, "antonymys_asp_c", antonyms_asp_c, "antonymys_tc_p", antonyms_tc_p, "antonymys_tc_c", antonyms_tc_c,
        "sim_asp_conclusion_asp_premise", [sim_asp_conclusion_asp_premise], "sim_tc_conclusion_asp_premise", [sim_tc_conclusion_asp_premise],
        "sim_tc_conclusion_premise", [sim_tc_conclusion_premise], "sim_asp_conclusion_tc_premise",[sim_asp_conclusion_tc_premise],
        "merged_tc_c_clean", merged_tc_c, "merged_tc_p_clean", merged_tc_p, "merged_asp_c_clean", merged_asp_c, "merged_asp_p_clean", merged_asp_p)

        arg_rel1 = Dam3ArgumentRelationAnalyzer._get_argument_relation_decomp(
            entailemt, antonyms_asp_p, antonyms_asp_c, antonyms_tc_p, antonyms_tc_c,
            sim_asp_conclusion_asp_premise, sim_tc_conclusion_asp_premise,
            sim_tc_conclusion_premise, sim_asp_conclusion_tc_premise,
            merged_tc_c, merged_tc_p, merged_asp_c, merged_asp_p
        )
        return arg_rel1

    @staticmethod
    def _calculate_similarity(components1, components2, similarity_function):
        similarity_scores = []
        for component1 in components1:
            component1 = component1.strip()
            if component1:
                for component2 in components2:
                    component2 = component2.strip()
                    if component2:
                        similarity_scores.append(similarity_function(component1, component2))
        if similarity_scores:
            return max(similarity_scores)
        return 0.0

    @staticmethod
    def _get_antonyms(components):
        antonyms = []
        for words in components:
            for word in words.split(" "):
                ants = " ".join(list(get_anotnyms_dam3(word)))
                antonyms.append(ants)
        return antonyms

    @staticmethod
    def _get_entailement(text1, text2):
        return get_entailement(text1, text2)

    @staticmethod
    def _get_functional_components_dam3(pair_of_propositions):
        extractor = FunctionalComponentsExtractor()
        return extractor.get_model_based_functional_components(pair_of_propositions)

    @staticmethod
    def _get_argument_relation_decomp(entailemt, antonyms_asp_p, antonyms_asp_c, antonyms_tc_p, antonyms_tc_c,
                                      sim_asp_conclusion_asp_premise, sim_tc_conclusion_asp_premise,
                                      sim_tc_conclusion_premise, sim_asp_conclusion_tc_premise,
                                      merged_tc_c, merged_tc_p, merged_asp_p, merged_asp_c):
        arg_rel2 = "None"

        if (sim_feature(sim_tc_conclusion_premise) and entailemt[0] > Dam3ArgumentRelationAnalyzer.THRESHOLD_SIMILARITY and
            sim_feature(sim_asp_conclusion_asp_premise)):
            arg_rel2 = "RA"
        elif (sim_feature(sim_tc_conclusion_premise) and entailemt[0] < Dam3ArgumentRelationAnalyzer.THRESHOLD_SIMILARITY and
              sim_feature(sim_asp_conclusion_asp_premise)):
            arg_rel2 = "CA"
        elif (sim_feature(sim_tc_conclusion_premise) and entailemt[0] > Dam3ArgumentRelationAnalyzer.THRESHOLD_SIMILARITY):
            arg_rel2 = "RA"
        elif (sim_feature(sim_asp_conclusion_tc_premise) and entailemt[0] > Dam3ArgumentRelationAnalyzer.THRESHOLD_SIMILARITY):
            arg_rel2 = "RA"
        elif (sim_feature(sim_asp_conclusion_asp_premise) and entailemt[0] < Dam3ArgumentRelationAnalyzer.THRESHOLD_SIMILARITY):
            arg_rel2 = "CA"
        elif (sim_feature(sim_asp_conclusion_asp_premise) and entailemt[0] > Dam3ArgumentRelationAnalyzer.THRESHOLD_SIMILARITY):
            arg_rel2 = "RA"
        elif (sim_feature(sim_asp_conclusion_asp_premise) and entailemt[0] > Dam3ArgumentRelationAnalyzer.THRESHOLD_SIMILARITY):
            arg_rel2 = "RA"
        elif (sim_feature(sim_tc_conclusion_asp_premise) and entailemt[0] > Dam3ArgumentRelationAnalyzer.THRESHOLD_SIMILARITY):
            arg_rel2 = "RA"
        elif (sim_feature(sim_tc_conclusion_premise) and entailemt[0] > Dam3ArgumentRelationAnalyzer.THRESHOLD_SIMILARITY and
              Dam3ArgumentRelationAnalyzer._are_anotnyms(antonyms_asp_c, merged_asp_p)):
            arg_rel2 = "CA"
        elif (sim_feature(sim_asp_conclusion_asp_premise) and entailemt[0] > Dam3ArgumentRelationAnalyzer.THRESHOLD_SIMILARITY and
              Dam3ArgumentRelationAnalyzer._are_anotnyms(antonyms_tc_c, merged_tc_p)):
            arg_rel2 = "CA"
        else:
            arg_rel2 = "None"

        return arg_rel2

    @staticmethod 
    def _are_anotnyms(string1,string2):
        if len(string1)==0 or len(string2)==0:
            return False
        for word in string1:
            if word in string2:
                return True
        return False

'''
#text1 = "there would be no non-tariff barriers with the deal done with the EU"
#text2 = "there are lots of non-tariff barriers with the deal done with the EU"
import pandas as pd

path = "/Users/debelagemechu/projects/argument mining/abstrct-master/AbstRCT_corpus/data/final.csv"
df = pd.read_csv(path)

p1s= list(set(df.proposition_1.values))
p2s = list(set(df.proposition_2.values))

propositions = p1s+p2s
c1s,a1s,c2s,a2s = [],[],[],[]


c_counts,a_counts = 0,0

for p1 in propositions:

    prediction = Dam3ArgumentRelationAnalyzer.get_argument_components((p1, p1)) 
    c1,c2,a1,a2 = prediction
    c1s.append(c1)
    a1s.append(a1)
    c_counts+=len(c1)
    a_counts+=len(a1)

df2 = pd.DataFrame(data={"propositions":propositions,
                         "target_concepts": c1s,
                         "aspects": a1s})
df2.to_csv("/Users/debelagemechu/projects/argument mining/abstrct-master/AbstRCT_corpus/data/decompositions.csv")
total_counts= {"target_concepts":c_counts,
             "aspects":a_counts}
print(total_counts)

#{'target_concepts': 15933, 'aspects': 15273}



'''