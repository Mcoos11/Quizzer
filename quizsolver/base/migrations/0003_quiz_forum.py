# Generated by Django 4.2.7 on 2024-01-28 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_quizresult_remove_quizanswer_question_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='forum',
            field=models.PositiveIntegerField(default=None, null=True, verbose_name='Forum (ID)'),
        ),
    ]
