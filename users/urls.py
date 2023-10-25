from django.urls import path
from .views import (
    login_view,
    logout_view,
    register_view,
    dashboard_view,
    password_change_view,
    password_reset_view,
    activate,
    passwordResetConfirm,
    profile_edit,
)

app_name = 'users'

urlpatterns = [
    path('login/', login_view, name='login-view'),
    path('logout/', logout_view, name='logout-view'),
    path('register/', register_view, name='register-view'),
    path('dashboard/', dashboard_view, name='dashboard-view'),
    path('settings/password-change/', password_change_view, name='password-change-view'),
    path('password-reset/', password_reset_view, name='password-reset-view'),
    path('reset/<uidb64>/<token>', passwordResetConfirm, name='password-reset-confirm'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('profile_edit/', profile_edit, name='profile-edit'),
]

# plik z przekierowaniami adresów do konkretnych funkcji lub klas widoków określonych w views.py
# wszystkie przekierowania opisane wyżej odbywają się wewnąrz aplikacji users