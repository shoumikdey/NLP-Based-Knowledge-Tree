from modules import *
from spacy.matcher import Matcher
from spacy.tokens import Span
from tika import parser
from tqdm import tqdm

import spacy
import csv
import nltk.data
import pandas as pd
from spacy import displacy
import os
import networkx as nx
import matplotlib.pyplot as plt


nlp = spacy.load('en_core_web_sm')

def main():
    pd.set_option('display.max_colwidth', 200)
    file = os.listdir("test_data"+os.sep)
    file = list(filter(lambda x: x[-4:] == '.pdf', file))
    parsedPDF = parser.from_file("test_data"+os.sep+str(file[0]))

    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    data = parsedPDF['content']
    fcsv = open('sent.csv', 'w')
    writer = csv.writer(fcsv, delimiter="\t")
    for sent in tokenizer.tokenize(data):
        writer.writerow([" ".join(sent.split())])
    sentences = pd.read_csv("sent.csv", sep= "\t", header=None, skip_blank_lines=True)
    sentences[0].shape

    sentences[0] = cleanup_text(sentences[0])

    sub_obj = []
    print("Reading", file[0])
    for i in tqdm(sentences[0]):
        sub_obj.append(entity_pair(i))
    print("Extracting relation and creating knowledge graph")
    rel = [get_relation(i) for i in tqdm(sentences[0])]
    #print(pd.Series(rel).value_counts()[:])

    src = [i[0] for i in sub_obj]
    target = [i[1] for i in sub_obj]

    kg_df = pd.DataFrame({'source':src, 'target':target, 'edge':rel})
    kg_df = kg_df[kg_df['edge']=="engine"]
    print(kg_df)
    G = nx.from_pandas_edgelist(kg_df, "source", "target", edge_attr=True, create_using=nx.MultiDiGraph())

    plt.figure(figsize=(12,12))
    pos = nx.spring_layout(G)
    nx.draw(G, with_labels=True, node_color='skyblue', edge_cmap=plt.cm.Blues, pos=pos)
    plt.show()

if __name__ == '__main__':
    main()
