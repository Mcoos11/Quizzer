from django.urls import path
from .views import QuizListView, QuizSolveView, QuizResultView, UserQuizResultsView

urlpatterns = [
    path('quizzes/', QuizListView.as_view(), name='quizzes'),
    path('solve/<int:quiz_pk>/', QuizSolveView.as_view(), name='solve'),
    path('results/<int:quiz_pk>/', QuizResultView.as_view(), name='results'),
    path('user_result/<int:user_id>/', UserQuizResultsView.as_view(), name='user_results')
]