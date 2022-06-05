from django.urls import path

from ads_list.views import ADSView, ADSDestroyAPIView

urlpatterns = [
    path('', ADSView.as_view(), name= 'ads-list' ),
    path('delete/<int:pk>', ADSDestroyAPIView.as_view(), name='ads-delete' )
    
]