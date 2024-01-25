from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nazwa kursu")
    author = models.PositiveIntegerField(null=True, verbose_name="Autor (ID)")
    category = models.CharField(max_length=100, verbose_name="Kategoria")
    description = models.TextField()


class Classroom(models.Model):
    owner = models.PositiveIntegerField(null=True, verbose_name="Owner")


class Files(models.Model):
    file_name = models.CharField(max_length=100)
    file = models.FileField(upload_to='import_course_files/')


class Class(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    attachments = models.ManyToManyField(Files, verbose_name="Zalaczniki")
