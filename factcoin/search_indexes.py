from haystack import indexes

from factcoin.models import Document


class DocumentIndex(indexes.ModelSearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    class Meta:
        model = Document

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
