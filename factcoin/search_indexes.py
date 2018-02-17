from haystack import indexes

from factcoin.models import Document


class DocumentIndex(indexes.ModelSearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(use_template=True)
    authors = indexes.CharField(use_template=True)
    localizations = indexes.CharField(use_template=True)
    people = indexes.CharField(use_template=True)
    organizations = indexes.CharField(use_template=True)

    class Meta:
        model = Document

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
