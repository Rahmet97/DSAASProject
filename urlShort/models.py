from django.contrib.sites.models import Site
from django.db import models


class UrlClicker(models.Model):
    ip_address = models.CharField(max_length=300)

    def __str__(self):
        return self.ip_address


class UrlShort(models.Model):
    original_url = models.URLField()
    slug = models.URLField(unique=True)
    clickers = models.ManyToManyField(to=UrlClicker)

    @property
    def get_clicks_count(self):
        return self.clickers.all().count()

    @property
    def get_short_url(self):
        return f"{Site.objects.get_current().domain}/ly/{self.slug}"

    def __str__(self):
        return f"Short Url for: {self.original_url} is {self.get_short_url}"
