
from argument_mining_framework.argument_relation.dam.models import ModelLoader

modelloader = ModelLoader()

def get_sentiment(text1,text2,sim_score=0.99):
	agree=False
	total_entailement1=""
	total_entailement2=""
	t1=modelloader.sentiment_classifier(text1)
	t1=t1[0]
	t2=modelloader.sentiment_classifier(text2)
	t2=t2[0]

	if t1['label']=="POSITIVE" and t1['score']>sim_score: 
		total_entailement1="POSITIVE"
	elif t1['label']=="NEGATIVE" and t1['score']>sim_score: 
		total_entailement1="NEGATIVE"
	else:
		total_entailement1="P_NEUTRAL"		
	if t2['label']=="POSITIVE" and t2['score']>sim_score: 
		total_entailement2="POSITIVE"
	elif t2['label']=="NEGATIVE" and t2['score']>sim_score: 
		total_entailement2="NEGATIVE"
	else:
		total_entailement2="P_NEUTRAL"	
	if((total_entailement1==total_entailement2) and (total_entailement2!="P_NEUTRAL" or total_entailement1!="P_NEUTRAL")):
		agree=True
	else:
		agree=False
	return agree