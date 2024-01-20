from rest_framework import serializers
from .models import Survey, SurveyQuestion, SurveyAnswer, SurveyFile

class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ("pk", "name", "topic", "author", "forum")

class SurveyQuestionSerializer(serializers.ModelSerializer):
    media = serializers.FileField(required=False)
    media_url = serializers.URLField(required=False)

    class Meta:
        model = SurveyQuestion
        fields = ("pk", "text", "survey", "answers_type", "media", "media_url")

class SurveyAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyAnswer
        fields = ("pk", "text", "correct", "question")

class SurveyFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyFile
        fields = ("file_name", "upload_time", "activated")