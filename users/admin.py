from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import User

# wyswietlanie modeli w panelu administracyjnym

class ProfileInline(admin.TabularInline):
    model = Profile

admin.site.unregister(User)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [ProfileInline]
