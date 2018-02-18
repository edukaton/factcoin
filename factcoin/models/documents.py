from __future__ import unicode_literals

from django.db import models
from factcoin.models.documents_utils import download_url, get_entities, get_feature_tokens, get_smiliar_documents
from factcoin.models.documents_utils import get_clickbait_rating, normalize_url
from factcoin.models.ratings_utils import update_rating, get_neighbours_score

import factcoin


class Document(models.Model):
    title = models.CharField(verbose_name='title', max_length=500)
    content = models.TextField(verbose_name='content', null=True)
    raw_content = models.TextField(verbose_name='content', null=True)
    authors = models.CharField(verbose_name='authors', null=True, max_length=500)
    localizations = models.TextField(verbose_name='localizations', null=True, max_length=500)
    people = models.TextField(verbose_name='localizations', null=True, max_length=500)
    organizations = models.TextField(verbose_name='localizations', null=True, max_length=500)
    timestamp = models.DateTimeField(null=True)
    url = models.URLField(verbose_name='url', null=True)

    def __str__(self):
        return self.title


    @property
    def rating_score(self):
        Rating = factcoin.models.ratings.Rating
        rating =  Rating.objects.filter(document=self).last()
        if rating:
            return rating.score
        else:
            return None


    @property
    def connections(self):
        Connection = factcoin.models.connections.Connection
        return Connection.get_document_connections(self)


    def add_vote(self, score):
        Vote = factcoin.models.votes.Vote
        vote = Vote.objects.create(document=self, score=score)
        self.update_rating()
        return vote


    def update_rating(self):
        rating = update_rating(self)
        return rating


    def get_similar_documents(self):
        Connection = factcoin.models.connections.Connection
        ids, scores = get_smiliar_documents(self)
        document_scores = dict(zip(ids, scores))

        documents = Document.objects.filter(id__in=ids)
        for document in documents:
            score = document_scores[document.id]
            Connection.create(self, document, score)
        return documents


    def get_evaluation(self):
        authors_score = 0
        if self.authors:
            authors_score = 1.0

        clickbait_score = get_clickbait_rating(self)[0]
        neighbours_score = get_neighbours_score(self)
        neighbours_count = self.connections.count()
        current_rating = 0.0
        current_rating = self.rating_score

        return clickbait_score, neighbours_score, neighbours_count, current_rating, authors_score


    @staticmethod
    def create(title, content, url, timestamp="", authors=""):
        document = Document.objects.create(title=title,
                                           content="",
                                           raw_content=content,
                                           authors=authors)

        #timestamp = timestamp,

        document.authors = " ".join(authors)
        document.content = " ".join(get_feature_tokens(content))
        document.url = normalize_url(url)

        entities = get_entities(content)
        document.organizations = " ".join(entities.get("I-ORG", ""))
        document.people = " ".join(entities.get("I-PER", ""))
        document.localizations = " ".join(entities.get("I-LOC", ""))
        return document


    @staticmethod
    def add_document_from_url(url):
        normalized_url = normalize_url(url)
        document = Document.objects.filter(url=normalized_url).first()
        if document:  # document already in the database
            document.get_similar_documents()
            return document, False
        else:
            json_data = download_url(normalized_url)
            document = Document.create(json_data["title"], json_data["text"],
                                       json_data["url"], json_data["timestamp"],
                                       json_data["authors"])
            document.get_similar_documents()
            document.save()
            return document, True


    @staticmethod
    def add_document_from_json(json_data):
        url = json_data["url"]
        document = Document.objects.filter(url=url).first()
        if document:  # document already in the database
            return document, False
        else:
            document = Document.create(json_data["title"], json_data["text"],
                                       json_data["url"], json_data["timestamp"],
                                       json_data["authors"])
            document.save()
            return document, True