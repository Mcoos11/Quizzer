from django.urls import path, include
from rest_framework import routers

from .views import (
    QuizView,
    QuestionView,
    UserQuizViewSet,
    QuizViewSet,
    QuestionViewSet,
    QuizQuestionViewSet,
    AllQuestionViewSet,
    PublicQuestionViewSet,
    AnswerView,
    AnswerViewSet,
    QuestionDeleteAll,
    
    file_question_upload,
    download_backup_csv,
    download_backup_xml,
)
main_router = routers.DefaultRouter()
main_router.register(r'^quiz', QuizView, basename='quiz')
main_router.register(r'user_quiz_set', UserQuizViewSet, basename='user_quiz_set')
main_router.register(r'^question', QuestionView, basename='question')
main_router.register(r'all_question_set', AllQuestionViewSet, basename='all_question_set')
main_router.register(r'public_question_set', PublicQuestionViewSet, basename='public_question_set')
main_router.register(r'delete_question_set', QuestionDeleteAll, basename='delete_question_set')
main_router.register(r'^answer', AnswerView, basename='answer')

app_name = 'editor'

urlpatterns = [
    path('', include(main_router.urls)),
    
    path('quiz_set/', QuizViewSet.as_view(), name='quiz_set'),
    path('quiz_questions_set/<int:quiz_pk>/', QuizQuestionViewSet.as_view(), name='quiz_question_set'),
    path('question_set/<int:quiz_pk>/', QuestionViewSet.as_view({'get': 'list'}), name='question_set'),
    path('file_question_upload/<int:quiz_pk>/', file_question_upload, name='file_question_upload'),
    path('download_backup_csv/<int:quiz_pk>/', download_backup_csv, name='download_backup_csv'),
    path('download_backup_xml/<int:quiz_pk>/', download_backup_xml, name='download_backup_xml'),
    path('answer_set/<int:question_pk>/', AnswerViewSet.as_view({'get': 'list'}), name='answer_set'),
    
]