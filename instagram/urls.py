from django.urls import path

from instagram.views import AccessTokenView, MainData


urlpatterns = [
    path('followers', MainData.as_view(), name="MainData"),
    path('access_token/', AccessTokenView.as_view())
]
