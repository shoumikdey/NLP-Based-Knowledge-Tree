from modules import *
from tika import parser
import spacy
import csv
import nltk.data
import re
import pandas as pd
import bs4
import requests
from spacy import displacy
nlp = spacy.load('en_core_web_sm')

from spacy.matcher import Matcher
from spacy.tokens import Span

import networkx as nx

import matplotlib.pyplot as plt
from tqdm import tqdm
pd.set_option('display.max_colwidth', 200)

parsedPDF = parser.from_file("FAA_Emergency_Procedures.pdf")

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

data = parsedPDF['content']
fcsv = open('sent.csv', 'w')
for sent in tokenizer.tokenize(data):
    #print(" ".join(sent.split()))
    fcsv.write(" ".join(sent.split()))
    fcsv.write("\n")

#reading from csv
sentences = pd.read_csv("sent.csv", sep= "\n", header=None, skip_blank_lines=True)
sentences[0].shape



#


# #
# doc = nlp("The failure indications of EFIS may be entirely different from conventional instruments making recognition of system malfunction much more difficult for the pilot.")
# for tok in doc:
#   print(tok.text, "...", tok.dep_)
# exit(0)


sub_obj = []
print(len(sentences[0]))
for i in tqdm(sentences[0]):
    sub_obj.append(entity_pair(i))

rel = [get_relation(i) for i in tqdm(sentences[0])]
print(pd.Series(rel).value_counts()[:50])
