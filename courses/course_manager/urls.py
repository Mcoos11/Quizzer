from django.urls import path

from .views import CourseViewSet, FileViewSet

urlpatterns = [
    path('courses', CourseViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('courses/<str:pk>', CourseViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('courses/<int:pk>/c<int:class_pk>/upload_file', FileViewSet.as_view({
        'post': 'create'
    })),
    path('courses/<int:pk>/download_file', FileViewSet.as_view({
        'get': 'retrieve'
    }))
]