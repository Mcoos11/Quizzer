from rest_framework import serializers
from .models import QuizResult


class QuizResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizResult
        fields = ['quiz', 'user', 'score', 'date', 'quiz_pass']