from django.contrib import admin
from .models import QuizAnswer, QuizQuestion, Quiz

# Register your models here.

admin.site.register(Quiz)

# dwie poniższe klasy do wyświetlania odpowiedzi 
# przy tworzeniu pytania w panelu admina
class AnswerInline(admin.TabularInline):
    model = QuizAnswer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

# widok pytań z odpowiedziami w panelu admina
admin.site.register(QuizQuestion, QuestionAdmin)

admin.site.register(QuizAnswer)