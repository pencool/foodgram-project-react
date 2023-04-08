from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager

USER_ROLE_CHOICE = (
    (settings.ADMIN, 'Администратор'),
    (settings.USER, 'Пользователь'),
)


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

    def create_superuser(self, username, email, password, **kwargs):
        user = self.create_user(username=username,
                                email=email,
                                password=password, **kwargs)
        user.role = settings.ADMIN
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractUser):
    """Костомная модель пользователя."""
    role = models.CharField(max_length=50, choices=USER_ROLE_CHOICE,
                            default='user')

    objects = MyUserManager()

    @property
    def is_admin(self):
        return self.role == settings.ADMIN or self.is_superuser

    @property
    def is_user(self):
        return self.role == settings.USER
