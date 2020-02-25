import spacy
nlp = spacy.load('en_core_web_sm')
from spacy.matcher import Matcher
from spacy.tokens import Span

def entity_pair(sent):
  ent1 = ""
  ent2 = ""

  prv_token_dep = ""    
  prv_token_text = ""

  prefix = ""
  modifier = ""


  for token in nlp(sent):
    if token.dep_ != "punct":
      if token.dep_ == "compound":
        prefix = token.text
        if prv_token_dep == "compound":
          prefix = prv_token_text + " "+ token.text

      if token.dep_.endswith("mod") == True:
        modifier = token.text
        if prv_token_dep == "compound":
          modifier = prv_token_text + " "+ token.text

      if token.dep_.find("subj") == True:
        ent1 = modifier +" "+ prefix + " "+ token.text
        prefix = ""
        modifier = ""
        prv_token_dep = ""
        prv_token_text = ""

      if token.dep_.find("obj") == True:
        ent2 = modifier +" "+ prefix +" "+ token.text

      prv_token_dep = token.dep_
      prv_token_text = token.text

  return [ent1.strip(), ent2.strip()]


def get_relation(sent):
    doc = nlp(sent)

    matcher = Matcher(nlp.vocab)

    pattern = [{'DEP':'ROOT'},
                {'DEP':'prep','OP':"?"},
                {'DEP':'agent','OP':"?"},
                {'POS':'ADJ','OP':"?"}]
    # pattern = [{'DEP':'nummod','OP':"?"},
    #        {'DEP':'amod','OP':"?"},
    #        {'POS':'NOUN'},
    #        {'IS_PUNCT':True},
    #        {'LOWER': 'especially'},
    #        {'DEP':'nummod','OP':"?"},
    #        {'DEP':'amod','OP':"?"},
    #        {'POS':'NOUN'}]
    matcher.add("matching_1", None, pattern)

    matches = matcher(doc)
    k = len(matches) - 1

    span = doc[matches[k][1]:matches[k][2]]
    return(span.text)
