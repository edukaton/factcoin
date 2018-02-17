from __future__ import unicode_literals

from django.db import models
from factcoin.models.documents_utils import download_url, get_entities, get_feature_tokens, get_smiliar_documents
from factcoin.models.documents_utils import get_clickbait_rating

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


    @staticmethod
    def create(title, content, url, timestamp="", authors=""):
        document = Document.objects.create(title=title,
                                           timestamp=timestamp,
                                           content="",
                                           raw_content=content,
                                           authors=authors)

        document.authors = " ".join(authors)
        document.content = " ".join(get_feature_tokens(content))
        document.url = url

        entities = get_entities(content)
        document.organizations = " ".join(entities.get("I-ORG", ""))
        document.people = " ".join(entities.get("I-PER", ""))
        document.localizations = " ".join(entities.get("I-LOC", ""))
        return document


    @staticmethod
    def add_document_from_url(url):
        document = Document.objects.filter(url=url).first()
        if document:  # document already in the database
            return document, False
        else:
            json_data = download_url(url)
            document = Document.create(json_data["title"], json_data["text"],
                                       json_data["url"], json_data["timestamp"],
                                       json_data["authors"])
            document.save()
            return document, True


    def get_similar_documents(self):
        ids, scores = get_smiliar_documents(self)
        documents = Document.objects.filter(id__in=ids)
        return documents


    def get_evaluation(self):
        authors_score = 0
        if self.authors:
            authors_score = 1.0
        clicbait_score = get_clickbait_rating(self)[0]
        return clicbait_score, authors_score


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