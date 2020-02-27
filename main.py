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
writer = csv.writer(fcsv, delimiter="\t")
for sent in tokenizer.tokenize(data):
    # print(" ".join(sent.split()))
#     fcsv.write(" ".join(sent.split()))
#     fcsv.write("\n")

    writer.writerow([" ".join(sent.split())])
#reading from csv
sentences = pd.read_csv("sent.csv", sep= "\t", header=None, skip_blank_lines=True)
sentences[0].shape



#


# #
# doc = nlp("The failure indications of EFIS may be entirely different from conventional instruments making recognition of system malfunction much more difficult for the pilot.")
# for tok in doc:
#   print(tok.text, "...", tok.dep_)
# exit(0)


sub_obj = []
for i in tqdm(sentences[0]):
    sub_obj.append(entity_pair(i))

rel = [get_relation(i) for i in tqdm(sentences[0])]
#print(pd.Series(rel).value_counts()[:])

src = [i[0] for i in sub_obj]
target = [i[1] for i in sub_obj]

kg_df = pd.DataFrame({'source':src, 'target':target, 'edge':rel})
kg_df = kg_df[kg_df['edge']=="engine"]
print(rel)
G = nx.from_pandas_edgelist(kg_df, "source", "target", edge_attr=True, create_using=nx.MultiDiGraph())

plt.figure(figsize=(12,12))
pos = nx.spring_layout(G)
nx.draw(G, with_labels=True, node_color='skyblue', edge_cmap=plt.cm.Blues, pos=pos)
plt.show()
