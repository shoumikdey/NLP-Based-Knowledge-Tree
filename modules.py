import spacy
nlp = spacy.load('en_core_web_sm')
from spacy.matcher import Matcher, PhraseMatcher
from spacy.tokens import Span
import string
from nltk.corpus import stopwords
import pandas as pd

def phrase_template():
    '''
    This function returns a list of all the possible technical terms that has high possibility of having several occurances in FAA handbooks and manuals,
    or in manuals pertaining to aircraft procedures and emergency procedures.

    This list is required to use the Phrase Matcher algoritm of matching the relations.
    '''
    phrases = ["emergency", "non-normal", " Federal Aviation Administration", "FAA", "Handbook", "emergency landings",
                "engine", "emergency landing", "forced landing", "precautionary landing", "ditching", "fire",
                "sink rate", "sink rate control", "attitude", "terrain selection", "safety concepts", "configuration",
                "approach", "terrain types", "terrain", "confined areas", "trees", "forest", "water", "snow", "after takeoff",
                "engine failure after takeoff", "single engine", "single-engine", "emergency descents", "in-flight", "in-flight fire",
                "engine fire", "electrical fire", "electrical fires", "cabin fire", "asymmetric", "split", "asymmetric flap", "asymmetric (split) flap", "flap", "flaps",
                "malfunction", "flight control malfunction", "flight control malfunctions", "flight control", "total flap failure", "total flaps failure",
                "loss", "loss of elevator control", "elevator", "elevator control", "gear", "landing gear", "landing gear malfunction", "gears", "systems malfunction", "systems malfunctions",
                "electrical", "electrical system", "pitot", "pitot-static", "pitot tube", "blocked", "blockage", "pitot-static system", "instrument operation", "pressure", "pressure chamber",
                "stall", "speed", "vertical speed", "door", "door opening in-flight", "door opeining", "loss", "loss of rpm", "rpm", "loss of manifold pressure", "gain of manifold pressure", "high oil temperature",
                "Inadvertent VFR Flight into IMC", "VFR Flight",  "VFR", "control", "maintaining", "airplane control", "maintaining airplane control",
                "attitude", "attitude indicator", "attitude control", "turns", "spiral", "graveyard spiral", "instabaility", "steep", "banks", "steep banks", "climbs", "descents", "maneuvers", "visual flight",
                "extend", "retract", "extension", "retraction", "non-instrument-rated", "pilot", "psychological hazards", "nose", "flying speed", "landing area", "throttle", "runway", "minimum", "touchdown", "glide",
                "damage", "groundspeed", "wind", "deceleration", "hydraulics", "hydraulic", "door", "opening", "spiral", "descent", "EFIS", "avionics", "IFR", "propellor", "thrust", "oil temperature", "oil pressure", "fuel pressure",
                "displays", "flight display", "cowl", "stall", "stall warning", "stall warning horn", "engines", "fuel", "fuel leak", "fuel shortage", "fuel tank", "fuel supply", "fuel selector", ]
    return phrases


def entity_pair(sent):

  '''
  The subject and the object is extracted from the sentence passed into the function.
  '''
  ent1 = ""
  ent2 = ""

  prev_token_dep = ""
  prev_token_text = ""

  prefix = ""
  modifier = ""


  for token in nlp(sent):
    if token.dep_ != "punct":
      if token.dep_ == "compound":
        prefix = token.text
        if prev_token_dep == "compound":
          prefix = prev_token_text + " "+ token.text

      if token.dep_.endswith("mod") == True:
        modifier = token.text
        if prev_token_dep == "compound":
          modifier = prev_token_text + " "+ token.text

      if token.dep_.find("subj") == True:
        ent1 = modifier +" "+ prefix + " "+ token.text
        prefix = ""
        modifier = ""
        prev_token_dep = ""
        prev_token_text = ""

      if token.dep_.find("obj") == True:
        ent2 = modifier +" "+ prefix +" "+ token.text

      prev_token_dep = token.dep_
      prev_token_text = token.text

  return [ent1.strip(), ent2.strip()]


def get_relation(sent):
    '''
    Relations are identified and matched in each sentence
    '''
    doc = nlp(sent)

    matcher = PhraseMatcher(nlp.vocab)
    pattern = list(nlp.tokenizer.pipe(phrase_template()))

    matcher.add("matching_1", None, *pattern)

    matches = matcher(doc)
    k = len(matches) - 1

    span = doc
    for match_id, start, end in matches:
        span = doc[start:end]


    return(span.text)

def cleanup_text(docs, logging=False):
    '''
    The text loaded from the PDF is cleaned and lemmatized. Entities such as Punctuations, stop words, pronouns etc are removed
    '''
    texts = []
    counter = 1

    for doc in docs:

        if counter % 1000 == 0 and logging:
            print("Processed %d out of %d documents." % (counter, len(docs)))

        counter += 1
        doc = nlp(doc, disable=['parser', 'ner'])

        tokens = [tok.lemma_.lower().strip() for tok in doc if tok.lemma_ != '-PRON-']
        tokens = [tok for tok in tokens if tok not in stopwords.words('english') and tok not in string.punctuation]
        tokens = ' '.join(tokens)

        texts.append(tokens)

    return pd.Series(texts)
