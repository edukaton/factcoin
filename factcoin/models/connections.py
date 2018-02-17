from __future__ import unicode_literals

from django.db import models
from factcoin.models.documents import Document


class Connection(models.Model):
    document1 = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="+")
    document2 = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="+")
    score = models.FloatField(default=0)

    def __str__(self):
        return "{} -> {}".format(self.document1, self.document2)

