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
    quiz_question_set,
    quiz_answer_set,
)
main_router = routers.DefaultRouter()
main_router.register(r'^quiz', QuizView, basename='quiz') #tworzenie/edycja/usuwanie quizu, do UPDATE i DELETE potrzebne pk quizu
main_router.register(r'user_quiz_set', UserQuizViewSet, basename='user_quiz_set') # zwaraca wszystkie quizy zalogowanego użytkownika 
main_router.register(r'^question', QuestionView, basename='question')# tworzenie/edycja/usuwanie pytania do UPDATE i DELETE potrzebne pk
main_router.register(r'all_question_set', AllQuestionViewSet, basename='all_question_set')# zwraca wszystkie dostępne pytania czyli takie, które są publiczne lub właścicielem jest zalogowany user
main_router.register(r'public_question_set', PublicQuestionViewSet, basename='public_question_set')# zwraca wszystkie publiczne pytania  
main_router.register(r'^delete_question_set', QuestionDeleteAll, basename='delete_question_set')# usuwanie wszystkich pytań w quizie przyjmuje pk quizu
main_router.register(r'^answer', AnswerView, basename='answer')# tworzenie/edycja/usuwanie odpowiedzi, do UPDATE i DELETE potrzebne pk

app_name = 'editor'

urlpatterns = [
    path('', include(main_router.urls)),
    
    path('quiz_set/', QuizViewSet.as_view(), name='quiz_set'),# zwaraca wszystkie quizy możliwe do wypęłnienia - takie które nie są w żadnym forum
    # path('quiz_questions_set/<int:quiz_pk>/', QuizQuestionViewSet.as_view(), name='quiz_question_set'),
    path('question_set/<int:quiz_pk>/', QuestionViewSet.as_view({'get': 'list'}), name='question_set'),# zwraca wszystkie pytania quizie
    path('file_question_upload/<int:quiz_pk>/', file_question_upload, name='file_question_upload'),# odbieranie formularza z przesłanm plikiem csv lub xml z pytaniami do dodania do quizu
    path('download_backup_csv/<int:quiz_pk>/', download_backup_csv, name='download_backup_csv'),#to i to następne wiadomo
    path('download_backup_xml/<int:quiz_pk>/', download_backup_xml, name='download_backup_xml'),
    path('answer_set/<int:question_pk>/', AnswerViewSet.as_view({'get': 'list'}), name='answer_set'),# zwraca wszystkie odpowiedzi danego pytania quizie
    path('quiz_question_set/<int:quiz_pk>/<str:pass_key>/', quiz_question_set, name='quiz_question_set'),# TO JEST DLA INNYCH USŁUG. Zwraca wszytkie pytania w danym quizie, nie sprawdza usera ale potrzebuje klucz dostępu
    path('quiz_answer_set/<int:question_pk>/<str:pass_key>/', quiz_answer_set, name='quiz_answer_set'),# TO JEST DLA INNYCH USŁUG. Zwraca wszytkie odpowiedzi w danym pytaniu, nie sprawdza usera ale potrzebuje klucz dostępu
    
]
