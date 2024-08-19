
#from src.argument_relation.predictor import ArgumentRelationPredictor

from src.argument_relation.predictor import ArgumentRelationPredictor as argument_relation


import json

# Example usage
if __name__ == "__main__":
    predictor = argument_relation("dialogpt", "vanila")

    xaif = {
        "AIF": {
            "nodes": [
                {"nodeID": "1", "text": "THANK YOU", "type": "I", "timestamp": "2016-10-31 17:17:34"},
                {"nodeID": "2", "text": "COOPER : THANK YOU", "type": "L", "timestamp": "2016-11-10 18:34:23"},
                {"nodeID": "3", "text": "You are well come", "type": "I", "timestamp": "2016-10-31 17:17:34"},
                {"nodeID": "4", "text": "Bob : You are well come", "type": "L", "timestamp": "2016-11-10 18:34:23"},
                {"nodeID": "5", "text": "does or doesn't Jeane Freeman think the SNP is divided with what is going on", "type": "I", "timestamp": ""},
                {"nodeID": "6", "text": "the SNP is a big party", "type": "I", "timestamp": ""},
                {"nodeID": "20", "text": "Default Inference", "type": "RA", "timestamp": ""},
                {"nodeID": "7", "text": "would or wouldn't Jeane Freeman describe the SNP as united", "type": "I", "timestamp": ""},
                {"nodeID": "8", "text": "the SNP has disagreements", "type": "I", "timestamp": ""},
                {"nodeID": "9", "text": "the SNP has disagreements", "type": "I", "timestamp": ""},
                {"nodeID": "10", "text": "Michael Forsyth belongs to a party that has disagreements", "type": "I", "timestamp": ""},
                {"nodeID": "11", "text": "one disagreement of Michael Forsyth's party is currently about their Scottish leader", "type": "I", "timestamp": ""},
                {"nodeID": "12", "text": "Iain Murray has had disagreements with his party", "type": "I", "timestamp": ""},
                {"nodeID": "13", "text": "it's not uncommon for there to be disagreements between party members", "type": "I", "timestamp": ""},
                {"nodeID": "14", "text": "disagreements between party members are entirely to be expected", "type": "I", "timestamp": ""},
                {"nodeID": "15", "text": "what isn't acceptable is any disagreements are conducted that is disrespectful of other points of view", "type": "I", "timestamp": ""},
                {"nodeID": "16", "text": "Jeanne Freeman wants to be in a political party and a country where different viewpoints and different arguments, Donald Dyer famously said, are conducted with respect and without abuse", "type": "I", "timestamp": ""},
                {"nodeID": "17", "text": "who does or doesn't Jeanne Freeman think is being disrespectful then", "type": "I", "timestamp": ""},
                {"nodeID": "18", "text": "people feel, when they have been voicing opinions on different matters, that they have been not listened to", "type": "I", "timestamp": ""},
                {"nodeID": "19", "text": "people feel that they have been treated disrespectfully. on all sides of the different arguments and disputes going on", "type": "L", "timestamp": ""}
            ],
            "edges": [
                {"edgeID": "1", "fromID": "1", "toID": "20", "formEdgeID": "None"},
                {"edgeID": "2", "fromID": "20", "toID": "3", "formEdgeID": "None"}
            ],
            "locutions": [],
            "participants": []
        },
        "text": "people feel that they have been treated disrespectfully. on all sides of the different arguments and disputes going on"
    }


    xaif = json.dumps(xaif)
    result_map = predictor.argument_map(xaif)
    print(result_map)


