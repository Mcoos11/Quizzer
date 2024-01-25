from django.contrib import admin
from django.urls import path

from .views import CourseViewSet

urlpatterns = [
    path('courses', CourseViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('courses/<str:pk>', CourseViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }))
]
