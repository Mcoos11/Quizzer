from django.db import models


class QuizResult(models.Model):
    quiz = models.PositiveIntegerField(null=True)
    user = models.PositiveIntegerField(null=True)
    score = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    quiz_pass = models.BooleanField(default=False)
