from django.db import models

from urlShort.models import UrlShort

from django.contrib.auth import get_user_model

User = get_user_model()


class ADS_list(models.Model):
    name = models.CharField(max_length=255)
    link = models.ForeignKey(UrlShort, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
    subscribes = models.FloatField()
    coverage = models.FloatField()
    view = models.FloatField()
    cost = models.FloatField()

    class Meta:
        verbose_name = "ADS_list calculate "
        verbose_name_plural = "ADS_list "

    def __str__(self):
        return str(self.name)
