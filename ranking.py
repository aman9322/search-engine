
# read the csv file
from fastbm25 import fastbm25
import json
import pandas as pd
import re
import enchant
import string
from num2words import num2words
from rank_bm25 import BM25Okapi
from bs4 import BeautifulSoup
import numpy as np
docs = pd.read_csv('leetcode_problems.csv')

# corpus = [doc.translate(str.maketrans('', '', string.punctuation)).replace('\n',"").lower() for doc in corpus]
# docs['problem_description'] = docs.fillna({'problem_description':''})

# corpus = [doc.translate(str.maketrans('', '', string.punctuation)).replace('\n',"").lower() for doc in docs['problem_description']]
# print(corpus[0:1])

# HTML Document
desc = []

# corpus = docs['problem_description']
cnt = 0
# print(corpus[0:2])
# df['data'] = df.fillna({'data':''}) write correct column name
docs = docs.fillna({
    'problem_title': '',
    'problem_description': '',
    'problem_link': ''
})


corpus = [doc.translate(str.maketrans('', '', string.punctuation)).replace('\n',"").lower() for doc in docs['problem_description']]
for doc in corpus:
    doc = re.sub('[^a-zA-Z0-9.?]',' ', doc)
    doc = doc.replace('  ',' ').lstrip().rstrip()
    doc = doc.split(' ')
    doc = [re.sub('(\d+)', lambda m: num2words(m.group()), sentence) for sentence in doc]
    d = enchant.Dict("en_US")
    doc = [el for el in doc if len(el)>1 and el.isalpha() and d.check(el)]
    
    desc.append(doc)

# print(desc[0])
title = []

corpus = [doc.translate(str.maketrans('', '', string.punctuation)).replace('\n',"").lower() for doc in docs['problem_title']]
for doc in corpus:
    doc = re.sub('[^a-zA-Z0-9.?]',' ', doc)
    doc = doc.replace('  ',' ').lstrip().rstrip()
    doc = doc.split(' ')
    doc = [re.sub('(\d+)', lambda m: num2words(m.group()), sentence) for sentence in doc]
    d = enchant.Dict("en_US")
    doc = [el for el in doc if len(el)>1 and el.isalpha() and d.check(el)]
    
    title.append(doc)

# print(title[0:4])

link = []
for doc in docs['problem_link']:
    link.append(doc)

# Print the extracted data

desc_bm = fastbm25(desc)
# title = BM25Okapi(title)
# link = BM25Okapi(link)

def get_scores(query : str):
    query = re.sub('[^a-zA-Z0-9.?]',' ', query)
    query = query.replace('  ',' ').lstrip().rstrip()
    query = query.split(' ')
    query = [re.sub('(\d+)', lambda m: num2words(m.group()), sentence) for sentence in query]
    d = enchant.Dict("en_US")
    query = [el for el in query if len(el)>1 and el.isalpha() and d.check(el)]
    
    results = desc_bm.top_k_sentence(query, k=5) 
    # print("results : ",results )
    index = []
    for i in range(0,len(results)):
        index.append(results[i][len(results[i])-2])
    # doc_scores = desc_bm.get_scores(query)
    # print(np.sort(doc_scores)[-4:][::-1] ) want top 5 scores
    # print(np.sort(doc_scores)[-5:][::-1] )

    # print(docs['problem_link'][index])
    # print(index)

    ranks = []
    for i in range(0,len(index)):
        # make json data and store in ranls
        # ranks.append("Rank :-"+str(i+1) , "  Title :"+docs['problem_title'][index]+" - "+docs['problem_link'][index])
        curr_rank = "Rank" + str(i+1)
        # make json dat
        ranks.append({curr_rank : { "Title" : docs['problem_title'][index[i]] , "Link" : docs['problem_link'][index[i]], "Score": results[i][len(results[i])-1]}})

    # print(ranks)
    return ranks
