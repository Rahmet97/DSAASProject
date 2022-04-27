from django.contrib.auth.models import BaseUserManager
from django.db import models


class UserManagerQuerySet(models.QuerySet):
    def company_admin(self):
        return self.filter(
            is_company_admin=True,
            whose_employee=None
        )


class UserManager(BaseUserManager):
    def get_queryset(self):
        return UserManagerQuerySet(self.model, using=self._db)

    def company_admin(self):
        return self.get_queryset().company_admin()

    def create_user(self, email, phone_number, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            phone_number=phone_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            phone_number=phone_number,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
