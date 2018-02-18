import os, pickle
from factcoin.settings.base import BASE_DIR
from polyglot.text import Text
import numpy as np
import factscraper
from urllib.parse import urlparse, urlunparse
import re
import requests

from pyelasticsearch import ElasticSearch


QUERY_TEXT = "text:{} OR title:{} OR people:{} OR localizations:{} OR organizations"

es = ElasticSearch('http://elasticsearch:9200')
tf_model_path = os.path.join(BASE_DIR, "shared", "vectorizer.pkl")
tf_model = pickle.load(open(tf_model_path, "rb"))

stopwords_path = os.path.join(BASE_DIR, "shared", "stopwords-pl.txt")
stopwords = open(stopwords_path).read().split('\n')

clickbait_vect_path = os.path.join(BASE_DIR, "shared", "clickbait_vectorizor.pkl")
clickbait_vect = pickle.load(open(clickbait_vect_path, "rb"))
clickbait_model_path = os.path.join(BASE_DIR, "shared", "clickbait_model.pkl")
clickbait_model = pickle.load(open(clickbait_model_path, "rb"))


def normalize_query(query):
    query = re.sub("[\[\]./!@#$%^&*\(\);<>]*", "", query)
    return query

def normalize_url(url):
    return url
    parsed_url = urlparse(url)
    url = urlunparse(
        ("",
         parsed_url.netloc,
         parsed_url.path,
         "", "", ""))
    return url


def download_url(url):
    return factscraper.parse(url)


def get_feature_tokens(text):
    doc = tf_model.transform([text])
    feature_names = tf_model.get_feature_names()
    tokens = [feature_names[i] for i in doc.indices]
    return tokens


def get_entities(text):
    entities = Text(text, hint_language_code='pl').entities
    results = {}
    for entity in entities:
        value = " ".join(entity._collection)
        results.setdefault(entity.tag, set())
        results[entity.tag].add(value)
    return results


def filter_stopwords(text):
    if not text:
        return text
    tokens = text.split()
    tokens = [token for token in tokens if token not in stopwords]
    return " ".join(tokens)


def get_smiliar_documents(doc):
    query_parts = []
    if doc.content:
        query_parts.append("text:{}".format(doc.content))
    if doc.title:
        query_parts.append("title:{}".format(doc.title))
    if doc.people:
        query_parts.append("people:{}".format(doc.people))
    if doc.localizations:
        query_parts.append("localizations:{}".format(doc.localizations))
    if doc.organizations:
        query_parts.append("organizations:{}".format(doc.organizations))

    query = " OR ".join(query_parts)
    query = normalize_query(query)

    ids, scores = [], []
    # print (es.search("test", index='haystack'))

    url = "http://elasticsearch:9200/haystack/_search?q={}".format(query)

    hits = {}
    try:
        hits = requests.get(url).json()
    except:
        pass

    if 'hits' in hits:
        for hit in hits['hits']['hits']:
            index = int(hit['_source']['id'].split('.')[-1])
            score = hit['_score']
            if index == doc.id:
                continue
            ids.append(index)
            scores.append(score)
    return ids, scores


def get_clickbait_rating(doc):
    X = clickbait_vect.transform([doc.raw_content])
    return clickbait_model.predict_proba(X)[0]
