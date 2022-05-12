from django.urls import path
from .views import UrlShortView, url_redirect

urlpatterns = [
    path('url/short', UrlShortView.as_view(), name='url-short'),
    path('<str:slugs>', url_redirect, name='url-redirect'),
]
