from django.urls import path
from .views import user_name_dict

app_name = 'base'

urlpatterns = [
    path('users_names_dict/', user_name_dict, name='user_name_dict')
]