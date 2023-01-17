from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return self.get_full_name()

    def __repr__(self):
        return f"<User '{self.username}' ('{self.get_full_name()}')>"
