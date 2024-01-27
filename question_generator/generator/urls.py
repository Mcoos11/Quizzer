from django.urls import path

from .views import (
    generate_XML,
    generate_CSV,
)

app_name = 'generator'

urlpatterns = [
    path('generate_XML/', generate_XML, name='XML'),
    path('generate_CSV/', generate_CSV, name='CSV'),
]