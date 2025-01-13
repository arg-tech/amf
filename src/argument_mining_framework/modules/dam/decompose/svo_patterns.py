from .subject_verb_object_extract import findSVOs, nlp
from nltk.corpus import stopwords


def get_dependecy_parsing_patterns(doc):
    tag_set = ['NNP', 'NN', 'VBP', 'NNS', 'JJ']
    sub, obj, opinion = [], [], []
    for token in doc:
        if (token.dep_ == 'nsubj' and token.tag_ in tag_set):
            sub.append(token.text)
        elif (token.dep_ == 'pobj' or token.dep_ == 'dobj') and  token.tag_ in tag_set:
            obj.append(token.text)
        elif (token.dep_ == 'amod' or token.dep_ == 'acomp' or token.dep_ == 'ROOT') and  token.tag_ in tag_set:
            opinion.append(token.text)
    return sub, opinion, obj


def decomposotionality_(doc): # return decompsitional elements for p
    sub=[]
    obj=[]
    opinion=[]

    for token in doc:

        if (token.dep_=='nsubj'):
            sub.append(token.text)
        # extract object
        elif (token.dep_=='pobj' or token.dep_=='dobj'):
            #print(token.text)
            obj.append(token.text)
        elif (token.dep_=='amod' or token.dep_=='acomp' or token.dep_=='ROOT'):

            opinion.append(token.text)
    return sub,opinion,obj


def get_components_svo(input_text):
    target_concept, aspect, opinion = [], [], []
    
    # Process the input text to obtain more elements
    doc = nlp(input_text)
    more_elements = get_dependecy_parsing_patterns(doc)
    
    # Extract SVO structures
    tok = nlp(input_text)
    svos = findSVOs(tok)
    comp = [list(elem) for elem in svos]    
    
    # Append more elements to the SVO structures
    comp += [list(elem) for elem in more_elements]
    
    # Remove stopwords and extract components
    for cmp in comp:
        if len(cmp) == 3:
            target_concept.append(cmp[0])
            opinion.append(cmp[1])
            aspect.append(cmp[2])
        elif len(cmp) == 2:
            target_concept.append(cmp[0])
            opinion.append(cmp[1])
    
    # Remove stopwords from the components
    cleaned_components = []
    for sublist in comp:
        cleaned_sublist = []
        for phrase in sublist:
            cleaned_phrase = " ".join([word.strip() for word in phrase.split() if word.strip() not in stopwords.words('english')])
            if cleaned_phrase:
                cleaned_sublist.append(cleaned_phrase.strip())
        cleaned_components.append(cleaned_sublist)
    
    return target_concept, aspect, opinion
