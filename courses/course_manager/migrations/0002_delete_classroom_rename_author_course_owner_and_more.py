# Generated by Django 4.2.7 on 2024-01-27 23:44

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course_manager', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Classroom',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='author',
            new_name='owner',
        ),
        migrations.RemoveField(
            model_name='class',
            name='attachments',
        ),
        migrations.AddField(
            model_name='class',
            name='course_id',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='course_manager.course'),
        ),
        migrations.AddField(
            model_name='course',
            name='participants',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(blank=True, default=None), null=True, size=None),
        ),
        migrations.AddField(
            model_name='files',
            name='class_id',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='course_manager.class'),
        ),
        migrations.AlterField(
            model_name='class',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='course',
            name='category',
            field=models.CharField(max_length=255, verbose_name='Kategoria'),
        ),
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Nazwa kursu'),
        ),
    ]
