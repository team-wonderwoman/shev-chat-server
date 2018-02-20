# Create your models here.

# -*- coding: utf-8 -*-
from django.db import models


class User(models.Model):
    user_email = models.CharField(max_length=45, unique=True)
    password = models.CharField(max_length=45)
    user_name = models.CharField(max_length=45)
    user_tel = models.CharField(max_length=45, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_email