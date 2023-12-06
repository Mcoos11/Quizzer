from django.shortcuts import render
from rest_framework import generics
from .models import Quiz
from .serializers import QuizSerializer

# Create your views here.

class QuizView(generics.CreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer