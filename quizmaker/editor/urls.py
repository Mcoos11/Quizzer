from django.urls import path
from .views import (
    QuizView
)

app_name = 'editor'

urlpatterns = [
    path("home", QuizView.as_view())
]