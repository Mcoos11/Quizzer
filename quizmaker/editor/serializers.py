from rest_framework import serializers
from .models import Quiz, QuizQuestion, QuizAnswer, QuizResult, QuizFile

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ("name", "topic", "number_of_questions", "max_time", "score_to_pass", "difficulty")