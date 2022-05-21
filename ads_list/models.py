from django.db import models

from urlShort.models import UrlShort

from django.contrib.auth import get_user_model

User = get_user_model()

class ADS_list(models.Model):
    name = models.CharField()
    ssilka = models.ForeignKey(UrlShort, on_delete=models.SET_NULL, null=True )
    type = models.CharField()
    vid = models.CharField()
    subscribe = models.IntegerField()
    oxvat = models.FloatField()
    cost = models.FloatField()

    class Meta:
        verbose_name = "ADS_list calculate "
        verbose_name_plural = "ADS_list "

    def __str__(self):
        return str(self.name) 




