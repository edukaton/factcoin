from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Document
from .serializers import DocumentSerializer


class DocumentMixin(object):
    permissions = (IsAuthenticatedOrReadOnly,)
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class DocumentList(DocumentMixin, generics.ListCreateAPIView):
    pass


class DocumentDetail(DocumentMixin, generics.RetrieveUpdateAPIView):
    pass
