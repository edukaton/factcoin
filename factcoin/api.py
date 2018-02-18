from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
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


class DocumentEvaluation(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        data = {}
        url = request.GET["url"]
        document, created = Document.add_document_from_url(url)
        clickbait_score, neighbours_score, neighbours_count, current_rating, authors_score = document.get_evaluation()

        data["id"] = document.id
        data["title"] = document.title
        data["text"] = document.raw_content
        data["authors"] = document.authors
        data["url"] = document.url
        data["clickbait_score"] = clickbait_score
        data["neighbours_score"] = neighbours_score
        data["neighbours_count"] = neighbours_count
        data["current_rating"] = current_rating
        data["authors_score"] = authors_score
        data["clickbait_spans"] = document.get_clickbait_spans()
        data["neighbours"] = document.neighbours

        data["created"] = created
        return Response(data)


class DocumentVote(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        data = {}
        url = request.GET["url"]
        score = request.GET["score"]
        document, created = Document.add_document_from_url(url)
        document.add_vote(score)

        data = {}
        data["id"] = document.id
        data["title"] = document.title
        data["url"] = document.url
        data["rating"] = document.rating_score
        return Response(data)
