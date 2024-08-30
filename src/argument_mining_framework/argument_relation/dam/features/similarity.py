from sentence_transformers import  util
from torch.nn import functional as F
#from src.models import (tokenizer, model,s_bert_model)
from nltk import pos_tag
from nltk.corpus import wordnet

from argument_mining_framework.argument_relation.dam.models import ModelLoader

modelloader = ModelLoader()

def get_anotnyms(word):
	tag_list = ["JJ","JJS","RB","IN","PRP"]
	wrd_tag = pos_tag([word])
	tag = wrd_tag[0][1]
	antonyms = [] 
	if(tag not in tag_list):	 
		for syn in wordnet.synsets(word): 
			for lema in syn.lemmas(): 
				if lema.antonyms(): 
					antonyms.append(lema.antonyms()[0].name()) 
	return set(antonyms)

def get_anotnyms_dam3(word):
	antonyms = [] 	 
	for syn in wordnet.synsets(word): 
		for lema in syn.lemmas(): 
			if lema.antonyms(): 
				antonyms.append(lema.antonyms()[0].name()) 
	return set(antonyms)

def similarity_aspect(sentence_rep, label_reps):
    return F.cosine_similarity(sentence_rep, label_reps)


def get_sim(comp1,comp2):
    embedding1 = modelloader.s_bert_model.encode(comp1, convert_to_tensor=True)
    embedding2 = modelloader.s_bert_model.encode(comp2, convert_to_tensor=True)
    sim_val = util.cos_sim(embedding1, embedding2)
    return(sim_val)

def get_sim_dam1_2(comp1,comp2):

    tag_list=["JJ","JJS","RB","IN","PRP"]
    decompositional_sim=[]
    subj12_anotnym=[]
    three_decompositional_sim=[]
    for cmp1 in comp1:
        for cm1s in cmp1:
            cm1_split=cm1s.split()
            sim_val=0
            data=[0]
            for cm1 in cm1_split:			
                for cmp2 in comp2: 
                    for cm2 in cmp2:                        
                        if(cm2 in list(set(get_anotnyms(cm1)))):
                            subj12_anotnym.append(1)
                        input_tag=[]
                        input_tag.append(cm1)
                        input_tag2=[]
                        input_tag2.append(cm2)

                        if  cm1:
                            wrd_tag1=pos_tag(input_tag)
                            wrd_tag2=pos_tag(input_tag2)
                            tag1=wrd_tag1[0][1]  
                            tag2=wrd_tag2[0][1] 
                            
                            if(tag1 not in tag_list and tag2 not in tag_list):
                                inputs = modelloader.tokenizer.batch_encode_plus([cm1] + cmp2,return_tensors='pt',pad_to_max_length=True)
                                input_ids = inputs['input_ids']
                                attention_mask = inputs['attention_mask']
                                output = modelloader.model(input_ids, attention_mask=attention_mask)[0]
                                sentence_rep = output[:1].mean(dim=1)
                                label_reps = output[1:].mean(dim=1)	            
                                similarities = F.cosine_similarity(sentence_rep, label_reps)
                                closest = similarities.argsort(descending=True)       					
            
                                for ind in closest:
                                    data.append(similarities[ind].item())
                                    decompositional_sim.append(similarities[ind].item())
                                sim_val=max(data, key=lambda item: item)  
                                print(sim_val)                    
                three_decompositional_sim.append(sim_val)
    return(three_decompositional_sim,subj12_anotnym)

def sim_feature(similarity, sim_score=0.80):
    if isinstance(similarity,list):
        for sim in similarity:
            if sim>sim_score:
                return True
    else:
        if similarity>sim_score:
            return True
         
    return False