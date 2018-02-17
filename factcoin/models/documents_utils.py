import os, pickle
from factcoin.settings.base import BASE_DIR
from polyglot.text import Text

import factscraper

tf_model_path = os.path.join(BASE_DIR, "shared", "vectorizer.pkl")
tf_model = pickle.load(open(tf_model_path, "rb"))


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
