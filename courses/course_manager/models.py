from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    description = models.TextField()


class User(models.Model):
    pass
