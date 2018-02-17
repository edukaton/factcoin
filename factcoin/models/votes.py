from __future__ import unicode_literals

from django.db import models
from factcoin.models.documents import Document


class Vote(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="votes")
    score = models.FloatField(default=0)

    def __str__(self):
        return "{} -> {}".format(self.document, self.vote)

