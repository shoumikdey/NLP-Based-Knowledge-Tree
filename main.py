from tika import parser
import spacy
import csv
import nltk.data
import re

parsedPDF = parser.from_file("FAA_Emergency_Procedures.pdf")

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

data = parsedPDF['content']
fcsv = open('sent.csv', 'w')
writer = csv.writer(fcsv, delimiter=',')
for sent in tokenizer.tokenize(data):
    print(" ".join(sent.split()))
    fcsv.write(" ".join(sent.split()))
    fcsv.write("\n")
    # writer.writerow('')
    #writer.writerow("Hello")



nlp = spacy.load('en_core_web_sm')
doc = nlp(parsedPDF['content'])
# for tok in doc:
  #print(tok.text, "...", tok.dep_)
