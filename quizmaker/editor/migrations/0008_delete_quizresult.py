# Generated by Django 4.2.7 on 2024-01-10 13:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0007_alter_quizquestion_media_url'),
    ]

    operations = [
        migrations.DeleteModel(
            name='QuizResult',
        ),
    ]
