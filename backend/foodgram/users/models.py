from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password, first_name, last_name,
                    **kwargs):
        if not username:
            raise ValueError('Имя пользователя должно быть заполнено.')
        if not email:
            raise ValueError('Email должен быть заполнен.')
        if not password:
            raise ValueError('Пароль должен быть заполнен.')
        if not first_name:
            raise ValueError('Имя должно быть заполнено.')
        if not last_name:
            raise ValueError('Фамилия должна быть заполнена.')
        user = self.model(username=username.lower(),
                          email=self.normalize_email(email),
                          **kwargs
                          )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, first_name='admin',
                         last_name='admin', **kwargs):
        user = self.create_user(username=username,
                                email=email,
                                password=password,
                                first_name=first_name,
                                last_name=last_name, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractUser):
    """Костомная модель пользователя."""
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    password = models.CharField(max_length=150)

    objects = MyUserManager()

    def __str__(self):
        return self.username
