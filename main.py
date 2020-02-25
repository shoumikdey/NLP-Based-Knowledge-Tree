from tika import parser
import spacy
import csv
import nltk.data
import re

parsedPDF = parser.from_file("FAA_Emergency_Procedures.pdf")

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

data = parsedPDF['content']

for sent in tokenizer.tokenize(data):
    print(" ".join(sent.split()))


nlp = spacy.load('en_core_web_sm')
doc = nlp(parsedPDF['content'])
# for tok in doc:
  #print(tok.text, "...", tok.dep_)
