from django.db import models


class User(models.Model):
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=128)
    mobile = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

