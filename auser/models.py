import binascii
import os

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _

from auser.managers import UserManager


class UserRole(models.Model):
    type = models.CharField(max_length=55)

    def __str__(self):
        return self.type


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name=_('email address'), max_length=255, unique=True)
    phone_number = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    type = models.ForeignKey(to=UserRole, on_delete=models.SET_NULL, null=True, blank=True)
    is_first_login = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_company_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Worker(models.Model):
    whose_employee = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="whose_employee")
    employee = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="employee")


class RecommendUserEmail(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=255, blank=True, null=True, unique=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_key()
        return super(RecommendUserEmail, self).save(*args, **kwargs)

    @property
    def is_invite_by_our_admin(self):
        """is invite by our admin (Digital saas)?"""
        return True

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()


class InviteUserEmail(models.Model):
    email = models.EmailField(unique=True, max_length=255)
    whose_employee_worker = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="invite_whose_employee")
    token = models.CharField(max_length=255, blank=True, null=True, unique=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_key()
        return super(InviteUserEmail, self).save(*args, **kwargs)

    @property
    def is_invite_by_our_admin(self):
        """is invite by our admin (Digital saas)?"""
        return False

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()
