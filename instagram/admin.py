from django.contrib import admin
from .models import Posts, InstaProfile

admin.site.register((Posts, InstaProfile))
