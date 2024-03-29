from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include("auser.urls")),
    path('task/', include('task_app.urls')),
    path('telegram/', include("telegram.urls")),
    path('v1/api/instagram/', include("instagram.urls")),
    path('ly/', include("urlShort.urls")),
    path('ads/', include("ads_list.urls")),
]

urlpatterns += doc_urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
