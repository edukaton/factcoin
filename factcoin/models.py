from __future__ import unicode_literals

from django.db import models


class Document(models.Model):
    title = models.CharField(verbose_name='title', max_length=500)
    content = models.TextField(verbose_name='content', null=True)
    authors = models.TextField(verbose_name='authors', null=True)
    url = models.URLField(verbose_name='url', null=True)

    def __str__(self):
        return self.title
