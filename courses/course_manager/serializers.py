from rest_framework import serializers
from .models import Course, Class, Files

class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ('name', 'owner', 'description', 'category', 'participants')


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = "__all__"
