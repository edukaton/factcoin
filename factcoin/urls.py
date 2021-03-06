"""factcoin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include, url

from .api import DocumentList, DocumentDetail, DocumentEvaluation, DocumentVote
from .views import HomeView


api_urlpatterns = [
    url(r'^document/$', DocumentList.as_view(), name='document-list'),
    url(r'^document/evaluation$', DocumentEvaluation.as_view(), name='document-evaluation'),
    url(r'^document/vote', DocumentVote.as_view(), name='document-vote'),
    url(r'^document/(?P<pk>\d+)/$', DocumentDetail.as_view(), name='document-detail'),
]

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^search/', include('haystack.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(api_urlpatterns))
]

