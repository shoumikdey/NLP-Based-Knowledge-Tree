import spacy
nlp = spacy.load('en_core_web_sm')
from spacy.matcher import Matcher, PhraseMatcher
from spacy.tokens import Span

def phrase_template():
    phrases = ["emergency", "non-normal", " Federal Aviation Administration", "Handbook", "emergency landings",
                "engine"]
    return phrases


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

    # matcher = Matcher(nlp.vocab)
    #
    # pattern = [{'DEP':'ROOT'},
    #             {'DEP':'prep','OP':"?"},
    #             {'DEP':'agent','OP':"?"},
    #             {'POS':'ADJ','OP':"?"}]

    matcher = PhraseMatcher(nlp.vocab)
    pattern = list(nlp.tokenizer.pipe(phrase_template()))
    # pattern = [{'DEP':'nummod','OP':"?"},
    #        {'DEP':'amod','OP':"?"},
    #        {'POS':'NOUN'},
    #        {'IS_PUNCT':True},
    #        {'LOWER': 'especially'},
    #        {'DEP':'nummod','OP':"?"},
    #        {'DEP':'amod','OP':"?"},
    #        {'POS':'NOUN'}]
    matcher.add("matching_1", None, *pattern)

    matches = matcher(doc)
    k = len(matches) - 1
    #
    #
    # print(len(matches))
    #span = doc[matches[0][1]:matches[0][2]]
    span = doc
    for match_id, start, end in matches:
        span = doc[start:end]
        #print(type(span))

    return(span.text)
