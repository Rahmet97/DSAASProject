from django.urls import path

from ads_list.views import ADS_listView

urlpatterns = [
    path('ads/', ADS_listView.as_view(), name= 'ads-list' ),
    
]