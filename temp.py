# coding: utf-8
from pyelasticsearch import ElasticSearch
import json


es = ElasticSearch('http://elasticsearch:9200')

raw = open("./shared/results.jsonl").read().split('\n')[:-1]
data = [json.loads(row) for row in raw]

for doc in data:
    es.index('documents', 'doc', doc)


es.search(text, index='haystack')

es.aliases
es.aliases.all()
es.aliases()



from sklearn.feature_extraction.text import TfidfVectorizer

tf = pickle.load(open("vectorizer.pkl", "rb"))

feature_names = tf.get_feature_names()

text = data[5]["text"]

import pickle

def get_feature_tokens(tf, text):
    doc = tf.transform([text])
    feature_names = tf.get_feature_names()
    tokens = [feature_names[i] for i in doc.indices]
    return (tokens)


from polyglot.text import Text

def get_entities(text):
    entities = Text(text, hint_language_code='pl').entities
    results = {}
    ORGs, PERs, LOCs = set(), set(), set()
    for entity in entities:
        value = " ".join(entity._collection)
        results.setdefault(entity.tag, set())
        results[entity.tag].add(value)
    return  results