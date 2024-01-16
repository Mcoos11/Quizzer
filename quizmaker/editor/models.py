from django.db import models
import random
from django.contrib.auth.models import User
from django.urls import reverse

# poniżej określono klasy na podstawie, których tworzone są odpowiednie tabele w bazie danych

DIFFICULTY_CHOICES = [
    ('łatwy', 'łatwy'),
    ('normalny', 'normalny'),
    ('trudny', 'trudny'),
]
ANSWERS_TYPE_CHOICES = [
    ('jednokrotny', 'jednokrotny'),
    ('wielokrotny', 'wielokrotny'),
]

class Quiz(models.Model):
    name = models.CharField(max_length=120, verbose_name="Nazwa")
    topic = models.CharField(max_length=120, verbose_name="Temat")
    author = models.PositiveIntegerField(null=True, verbose_name="Autor (ID)")
    forum = models.PositiveIntegerField(null=True, default=None, verbose_name="Forum (ID)")
    number_of_questions = models.PositiveIntegerField(help_text="Liczba pytań w jednym podejściu", verbose_name="Liczba pytań")
    max_time = models.IntegerField(help_text="Maksymalny czas trwania tesu [min]", default=1, verbose_name="Czas na rozwiązanie")
    score_to_pass = models.PositiveIntegerField(help_text="Punkty wymagane do zaliczenia quizu [%]", verbose_name="Punkty wymagane do zaliczenia")
    created_time = models.DateTimeField(auto_now_add=True)
    difficulty = models.CharField(max_length=9 , choices=DIFFICULTY_CHOICES, verbose_name="Poziom trudności")

    def __str__(self):
        return f"{self.name}-{self.topic} [Quiz]"

    def get_questions(self):
        questions = list(self.questions.all())
        random.shuffle(questions)
        return questions[:self.number_of_questions]
    
    def get_absolute_url(self):
        return reverse('quizzes:edit-menu')

    class Meta:
        verbose_name_plural = "Quizzes"

class QuizQuestion(models.Model):
    text = models.CharField(max_length=200)
    quiz = models.ManyToManyField(Quiz, related_name="questions")
    author = models.PositiveIntegerField(null=True, verbose_name="Autor (ID)")
    answers_type = models.CharField(max_length=11, choices=ANSWERS_TYPE_CHOICES, default='jednokrotny')
    created_time = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=False)
    media = models.FileField(null=True, blank=True, upload_to="question_media/")
    media_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return str(self.text) + " [Question]"

    def get_answers(self):
        answers = list(self.answers.all())
        random.shuffle(answers)
        return answers

class QuizAnswer(models.Model):
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name="answers")

    def __str__(self):
        return f"question: {self.question.text}, answer: {self.text}, correct: {self.correct} [Answer]"
    
class QuizFile(models.Model):
    file_name = models.FileField(upload_to='import_quizzes_files/')
    upload_time = models.DateTimeField(auto_now_add=True)
    # po przesłaniu pliku activated pozostanie False do puki
    # informacje z pliku nie zostaną załadowane do bazy
    activated = models.BooleanField(default=False) 

    def __str__(self):
        return f"ID: {self.pk}, Nazwa: {self.file_name}"
