from os.path import splitext

from django.db import models
from transliterate.utils import slugify

from auser.models import User


class TGChannel(models.Model):
    link = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Telegram Channel or Group"
        verbose_name_plural = "Telegram Channels and Groups"

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


def slugify_upload(instance, filename):
    folder = instance._meta.model.__name__
    name, ext = splitext(filename)
    try:

        name_t = slugify(name)
        if name_t is None:
            name_t = name
        path = folder + "/" + name_t + ext
    except:
        path = folder + "/default" + ext

    return path


class Post(models.Model):
    date = models.DateTimeField()
    link = models.URLField()
    link_name = models.CharField(max_length=50)
    description = models.TextField()
    hashtag = models.CharField(max_length=255)
    file = models.FileField(upload_to=slugify_upload)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Post of auto post telegram"
        verbose_name_plural = "Posts"

    def __str__(self):
        return str(self.date)
