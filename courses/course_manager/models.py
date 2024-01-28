from django.contrib.postgres.fields import ArrayField
from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nazwa kursu")
    owner = models.PositiveIntegerField(verbose_name="Autor (ID)")
    category = models.CharField(max_length=255, verbose_name="Kategoria")
    description = models.TextField()
    participants = ArrayField(models.PositiveIntegerField(blank=True, default=None), null=True)


class Class(models.Model):
    k_course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, default=None)
    name = models.CharField(max_length=255)
    description = models.TextField()


class Files(models.Model):
    k_course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, default=None)
    k_class = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, default=None)
    file_name = models.CharField(max_length=100)
    file = models.FileField(upload_to='import_course_files/')
