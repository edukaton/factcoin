from __future__ import unicode_literals

from django.db import models
from factcoin.models.documents_utils import download_url, get_entities, get_feature_tokens


class Document(models.Model):
    title = models.CharField(verbose_name='title', max_length=500)
    content = models.TextField(verbose_name='content', null=True)
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
                                           authors=authors)

        return document


    @staticmethod
    def add_document_from_url(url):
        document = Document.objects.filter(url=url).first()
        if document:  # document already in the database
            return document, True
        else:
            json_data = download_url(url)
            document = Document.create(**json_data)
            document.save()
            return document, False


    @staticmethod
    def add_document_from_json(json_data):
        url = json_data["url"]
        document = Document.objects.filter(url=url).first()
        if document:  # document already in the database
            return document, True
        else:
            document = Document.create(**json_data)
            document.save()
            return document, False