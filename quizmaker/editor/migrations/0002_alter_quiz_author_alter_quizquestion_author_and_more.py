# Generated by Django 4.2.7 on 2024-01-01 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='author',
            field=models.PositiveIntegerField(null=True, verbose_name='Autor (ID)'),
        ),
        migrations.AlterField(
            model_name='quizquestion',
            name='author',
            field=models.PositiveIntegerField(null=True, verbose_name='Autor (ID)'),
        ),
        migrations.AlterField(
            model_name='quizresult',
            name='user',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
