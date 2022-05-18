from os.path import splitext

from django.db import models
from transliterate.utils import slugify

from auser.models import User


class InstaProfile(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Instagram Profile"
        verbose_name_plural = "Instagram Profiles"

    def __str__(self):
        return self.username


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


class Posts(models.Model):
    date = models.DateTimeField()
    location = models.CharField(max_length=30)
    marking = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to=slugify_upload)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Post of auto post Instagram"
        verbose_name_plural = "Posts"

    def __str__(self):
        return str(self.date)
