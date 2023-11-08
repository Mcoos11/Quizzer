from django.db import models
from django.contrib.auth.models import User

# poniżej określono klasy na podstawie, których tworzone są odpowiednie tabele w bazie danych
STATUS_CHOICES = [
    ('otwarty', 'otwarty'),
    ('zamknięty', 'zamknięty'),
]


class Topic(models.Model):
    name = models.CharField(max_length=200, verbose_name="Temat")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=9 , choices=STATUS_CHOICES, verbose_name="Status")
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        NO_USER = 'no-user'
        return f'{self.owner.username if self.owner else NO_USER}-{self.pk}'
    
class Entry(models.Model):
    text = models.TextField(verbose_name='Treść', max_length=2000)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Entry | {self.pk}'
