from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# poniżej określono klasy na podstawie, których tworzone są odpowiednie tabele w bazie danych

ANSWERS_TYPE_CHOICES = [
    ('jednokrotny', 'jednokrotny'),
    ('wielokrotny', 'wielokrotny'),
]

REPETITION_PROTECT_CHOICES = [
    ('adres_ip', 'Adres IP'),
    ('konto_urzytkownika', 'Konto urzytkownika'),
    ('dostep_otwarty', 'Dostęp otwarty'),
]

class Survey(models.Model):
    topic = models.CharField(max_length=120, verbose_name="Temat ankiety")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Właściciel")
    description = models.TextField(max_length=250, default="", verbose_name="Opis ankiety")
    status = models.BooleanField(default=False, verbose_name="Status ankiety")
    anonymity = models.BooleanField(default=False, verbose_name="Anonimowość")
    created_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateField(auto_now_add=False, null=True, blank=True, verbose_name="Data zakończenia ankiety")
    repetition_protect = models.CharField(max_length=19, choices=REPETITION_PROTECT_CHOICES, default='adres_ip')

    def __str__(self):
        return f"{self.topic} [Survey]"
    
    def get_questions(self):
        questions = list(self.questions.all())
        return questions
    
    def get_absolute_url(self):
        return reverse('surveys:survey-list-view')
    
class SurveyQuestion(models.Model):
    text = models.CharField(max_length=200)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="questions")
    answers_type = models.CharField(max_length=11, choices=ANSWERS_TYPE_CHOICES, default='jednokrotny')
    image = models.ImageField(null=True, blank=True, upload_to="survey_question_images/")

    def __str__(self):
        return str(self.text) + " [SurveyQuestion]"

    def get_answers(self):
        answers = list(self.answer_set.all())
        return answers

class Answer(models.Model):
    text = models.CharField(max_length=200)
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    other = models.BooleanField(default=False)
    user_answer = models.BooleanField(default=False)

    def __str__(self):
        return f"question: {self.question.text}, answer: {self.text} [Answer]"

class UserDone(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.pk) + "[UserDone]"

class SurveyResult(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.pk) + "[Result]"
    
class SelectedAnswer(models.Model): 
    text = models.CharField(max_length=200)
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    result = models.ForeignKey(SurveyResult, on_delete=models.CASCADE)
    user_answer = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk) + "[SelectedAnswer]"

class SurveyFile(models.Model):
    file_name = models.FileField(upload_to='import_survey_files/')
    upload_time = models.DateTimeField(auto_now_add=True)
    # po przesłaniu pliku activated pozostanie False do puki
    # informacje z pliku nie zostaną załadowane do bazy
    activated = models.BooleanField(default=False) 

    def __str__(self):
        return f"ID: {self.pk}, Nazwa: {self.file_name}"