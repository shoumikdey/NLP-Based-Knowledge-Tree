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

# Loading the english model from spacy
nlp = spacy.load('en_core_web_sm')

def main():
    '''
    The input pdf is taken from the test_data folder.
    Only one file will be read from this folder if multiple files are present.
    The file that appers first in the alphabetical order will be read and others will be ignored.
    '''

    pd.set_option('display.max_colwidth', 200)
    file = os.listdir("test_data"+os.sep)
    file = list(filter(lambda x: x[-4:] == '.pdf', file))
    if not file:
        exit("No PDF found !")
    parsedPDF = parser.from_file("test_data"+os.sep+str(file[0]))

    '''
    The PDF document is being parsed here and all the text(only) is extracted
    and tokenized.

    From the text, it is next tokenized into sentences using the natural language toolkit nltk.
    '''

    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    data = parsedPDF['content']
    fcsv = open('sent.csv', 'w')
    writer = csv.writer(fcsv, delimiter="\t")
    for sent in tokenizer.tokenize(data):
        writer.writerow([" ".join(sent.split())])
    sentences = pd.read_csv("sent.csv", sep= "\t", header=None, skip_blank_lines=True)
    sentences[0].shape


    sentences[0] = cleanup_text(sentences[0])
    '''
    Cleaning of the sentences extracted. Punctuations, stop words, pronouns etc are removed
    so that they do not produce false positives
    '''

    sub_obj = []
    print("Reading", file[0])
    for i in tqdm(sentences[0]):
        sub_obj.append(entity_pair(i))
    print()
    print("Extracting relation and creating knowledge graph")
    rel = [get_relation(i) for i in tqdm(sentences[0])]

    '''
    The entity pairs (subject, object) from each sentence is extracted and the relation for each node
    of the knowledge graph is obtained.
    '''

    src = [i[0] for i in sub_obj]
    target = [i[1] for i in sub_obj]

    kg_df = pd.DataFrame({'source':src, 'target':target, 'edge':rel}) # The relations obtained are appended into a pandas dataframe for the visualisation of the knowledge graph
    print()
    print("Enter the name of the system")
    print("Example inputs: 'engine', 'fire', 'flap', 'electrical', 'fuel', 'gear'")
    inp = input("just press enter to display the full graph: ")
    if inp != "":
        kg_df = kg_df[kg_df['edge']==str(inp)]
    print(kg_df)
    G = nx.from_pandas_edgelist(kg_df, "source", "target", edge_attr=True, create_using=nx.MultiDiGraph())

    plt.figure(figsize=(12,12))
    pos = nx.spring_layout(G)
    nx.draw(G, with_labels=True, node_color='blue', edge_cmap=plt.cm.Blues, pos=pos)
    plt.show() # displaying the processed knowledge graph

if __name__ == '__main__':
    main()
