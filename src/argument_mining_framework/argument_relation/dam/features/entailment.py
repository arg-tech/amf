
from argument_mining_framework.argument_relation.dam.models import ModelLoader

modelloader = ModelLoader()
def predict_entailement(text1,text2):
	total_entailement2=[]
	input_ids = modelloader.tokenizer_enatilement.encode(text1, text2, return_tensors='pt')
	logits = modelloader.model_enatilement(input_ids)[0]
	entail_contradiction_logits = logits[:,[0,2]]
	probs = entail_contradiction_logits.softmax(dim=1)
	true_prob = probs[:,1].item() * 100
	total_entailement2.append(true_prob)
	return (total_entailement2)

def get_entailement(text1,text2):

    entailemt_1=predict_entailement(text1,text2)# 
    entailemt_2=predict_entailement(text2,text1)
    if(entailemt_1[0]>=entailemt_2[0]):    
        entailemt=entailemt_1			
    if(entailemt_2[0]>=entailemt_1[0]):    
        entailemt=entailemt_2 
    return entailemt


