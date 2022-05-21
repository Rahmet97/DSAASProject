from django.contrib import admin
from .models import Post, TGChannel

admin.site.register((Post, TGChannel))
