from django.urls import path

from .views import CourseViewSet, FileViewSet, ClassViewSet

urlpatterns = [
    path('courses', CourseViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('courses/<int:pk>', CourseViewSet.as_view({
        'put': 'update',
        'delete': 'destroy',
        'get': 'retrieve',
        'post': 'add_user'
    })),
    path('courses/<int:pk>/files', FileViewSet.as_view({
        'get': 'list'
    })),
    path('courses/<int:pk>/c<int:class_pk>', ClassViewSet.as_view({
        'post': 'add_class',
        'delete': 'delete_class'
    })),
    path('courses/<int:pk>/c<int:class_pk>/upload_file', FileViewSet.as_view({
        'post': 'create'
    })),
    path('courses/<int:pk>/download_file', FileViewSet.as_view({
        'get': 'retrieve'
    }))
]