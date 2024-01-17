from django.db import models
import random
from django.urls import reverse

# poniżej określono klasy na podstawie, których tworzone są odpowiednie tabele w bazie danych

ANSWERS_TYPE_CHOICES = [
    ('jednokrotny', 'jednokrotny'),
    ('wielokrotny', 'wielokrotny'),
]

class Survey(models.Model):
    name = models.CharField(max_length=120, verbose_name="Nazwa")
    topic = models.CharField(max_length=120, verbose_name="Temat")
    author = models.PositiveIntegerField(null=True, verbose_name="Autor (ID)")
    forum = models.PositiveIntegerField(null=True, default=None, verbose_name="Forum (ID)")
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}-{self.topic} [Survey]"
    
    def get_questions(self):
        return list(self.questions.all())

class SurveyQuestion(models.Model):
    text = models.CharField(max_length=200)
    survey = models.ManyToManyField(Survey, related_name="questions")
    answers_type = models.CharField(max_length=11, choices=ANSWERS_TYPE_CHOICES, default='jednokrotny')
    created_time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False, verbose_name="Status ankiety")
    media = models.FileField(null=True, blank=True, upload_to="question_media/")
    media_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return str(self.text) + " [Question]"

    def get_answers(self):
        answers = list(self.answers.all())
        random.shuffle(answers)
        return answers

class SurveyAnswer(models.Model):
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE, related_name="answers")
    user_answer = models.BooleanField(default=False)

    def __str__(self):
        return f"question: {self.question.text}, answer: {self.text}, correct: {self.correct} [Answer]"
    
class SurveyFile(models.Model):
    file_name = models.FileField(upload_to='import_surveys_files/')
    upload_time = models.DateTimeField(auto_now_add=True)
    # po przesłaniu pliku activated pozostanie False do puki
    # informacje z pliku nie zostaną załadowane do bazy
    activated = models.BooleanField(default=False) 

    def __str__(self):
        return f"ID: {self.pk}, Nazwa: {self.file_name}"