from django.contrib import admin
from .models import UrlClicker, UrlShort


@admin.register(UrlShort)
class UrlShortAdmin(admin.ModelAdmin):
    readonly_fields = ['get_short_url', 'get_clicks_count']


admin.site.register(UrlClicker)
