from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.db import models

User = get_user_model()


class UrlClicker(models.Model):
    ip_address = models.CharField(max_length=300)

    def __str__(self):
        return self.ip_address


class UrlShort(models.Model):
    director_user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
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
