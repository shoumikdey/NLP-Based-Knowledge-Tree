from tika import parser
import spacy
import csv
import nltk.data
import re

parsedPDF = parser.from_file("FAA_Emergency_Procedures.pdf")

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
# fp = open("test.txt")
data = parsedPDF['content']
#print('\n-----\n'.join(tokenizer.tokenize(data)))
# s = tokenizer.tokenize(data)
# print(" ".join(s[-2].split()))
# exit(0)
for sent in tokenizer.tokenize(data):
    print(" ".join(sent.split()))


nlp = spacy.load('en_core_web_sm')
#doc = nlp("A well-executed water landing normally involves less deceleration violence than a poor tree landing or a touchdown on extremely rough terrain. Also, an airplane that is ditched at minimum speed and in a normal landing attitude does not immediately sink upon touchdown. Intact wings and fuel tanks (especially when empty) provide floatation for at least several minutes, even if the cabin may be just below the water line in a high-wing airplane.")
doc = nlp(parsedPDF['content'])
# for tok in doc:
  #print(tok.text, "...", tok.dep_)
