from django.urls import path
from .views import QuizListView, QuizSolveView, QuizResultView

urlpatterns = [
    path('quizzes/', QuizListView.as_view(), name='quizzes'),
    path('solve/<int:quiz_pk>/', QuizSolveView.as_view(), name='solve'),
    path('results/<int:quiz_pk>/', QuizResultView.as_view(), name='results')
]