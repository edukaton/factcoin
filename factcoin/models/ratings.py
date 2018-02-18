from __future__ import unicode_literals

from django.db import models
from factcoin.models.documents import Document


class Rating(models.Model):
    parent = models.OneToOneField(Document, on_delete=models.SET_NULL, related_name="+", null=True, blank=True)
    document = models.OneToOneField(Document, on_delete=models.CASCADE, related_name="rating")
    score = models.FloatField(default=0)

    def __str__(self):
        return "{} - score: {}".format(self.document, self.rating)

