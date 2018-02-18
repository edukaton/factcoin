from __future__ import unicode_literals

from django.db import models
from factcoin.models.documents import Document
from django.db.models import Q


class Connection(models.Model):
    document1 = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="+")
    document2 = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="+")
    score = models.FloatField(default=0)

    def __str__(self):
        return "{} -> {}".format(self.document1, self.document2)

    def get_other(self, document):
        if self.document1 == document:
            return self.document2
        elif self.document2 == document:
            return self.document1
        else:
            return None

    @staticmethod
    def get_document_connections(document):
        return Connection.objets.filter(Q(document1=document) | Q(document2=document))


    @staticmethod
    def create(document1, document2, score):
        connection = Connection.objets.filter(Q(document1=document1) | Q(document2=document1))
        connection = connection.filter(Q(document1=document2) | Q(document2=document2)).first()

        if not connection:
            connection = Connection.objects.create(document1=document1, document2=document2)

        connection.score = score

        return connection
