from rest_framework import serializers

class RequestSerializer(serializers.Serializer):
    questions_number = serializers.IntegerField()
    topic = serializers.CharField()
    answers_number = serializers.IntegerField(required=False)
    url = serializers.URLField(required=False)
