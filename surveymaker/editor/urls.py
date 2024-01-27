from django.urls import path, include
from rest_framework import routers

from .views import (
    SurveyView,
    QuestionView,
    UserSurveyViewSet,
    SurveyViewSet,
    QuestionViewSet,
    SurveyQuestionViewSet,
    AnswerView,
    AnswerViewSet,
    QuestionDeleteAll,
    
    file_question_upload,
    download_backup_csv,
    download_backup_xml,
    survey_question_set,
    survey_answer_set,
)
main_router = routers.DefaultRouter()
main_router.register(r'^survey', SurveyView, basename='survey')
main_router.register(r'user_survey_set', UserSurveyViewSet, basename='user_survey_set')
main_router.register(r'^question', QuestionView, basename='question')
main_router.register(r'delete_question_set', QuestionDeleteAll, basename='delete_question_set')
main_router.register(r'^answer', AnswerView, basename='answer')

app_name = 'editor'

urlpatterns = [
    path('', include(main_router.urls)),
    
    path('survey_set/', SurveyViewSet.as_view(), name='survey_set'),
    # path('survey_questions_set/<int:survey_pk>/', SurveyQuestionViewSet.as_view(), name='survey_question_set'),
    path('question_set/<int:survey_pk>/', QuestionViewSet.as_view({'get': 'list'}), name='question_set'),
    path('file_question_upload/<int:survey_pk>/', file_question_upload, name='file_question_upload'),
    path('download_backup_csv/<int:survey_pk>/', download_backup_csv, name='download_backup_csv'),
    path('download_backup_xml/<int:survey_pk>/', download_backup_xml, name='download_backup_xml'),
    path('answer_set/<int:question_pk>/', AnswerViewSet.as_view({'get': 'list'}), name='answer_set'),
    path('survey_question_set/<int:survey_pk>/<str:pass_key>/', survey_question_set, name='survey_question_set'),
    path('survey_answer_set/<int:question_pk>/<str:pass_key>/', survey_answer_set, name='survey_answer_set'),
    
]