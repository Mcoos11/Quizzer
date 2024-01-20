from rest_framework import serializers
from .models import Quiz, QuizQuestion, QuizAnswer, QuizFile

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ("pk", "name", "topic", "number_of_questions", "max_time", "score_to_pass", "difficulty", "author", "forum")

class QuizQuestionSerializer(serializers.ModelSerializer):
    media = serializers.FileField(required=False)
    media_url = serializers.URLField(required=False)

    class Meta:
        model = QuizQuestion
        fields = ("pk", "text", "quiz", "author", "answers_type", "media", "media_url")

class QuizAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAnswer
        fields = ("pk", "text", "correct", "question")

class QuizFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizFile
        fields = ("file_name", "upload_time", "activated")
