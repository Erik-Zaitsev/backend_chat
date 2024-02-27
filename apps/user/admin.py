from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, CustomUserManager


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):  
    list_display = [
        'username',
        'email',
        'date_joined',
        'last_login',
        'is_staff',
        'is_superuser',
        'is_active',
    ]
    
    list_filter = ('is_staff', 'is_superuser',)
    
    search_fields = ['username', ]
    
    search_help_text = 'Поиск по полям: Пользователь'
    
    readonly_fields = ['date_joined', 'last_login',]
    
    fieldsets = (
        ('Персональная информация',
        {'fields': ('username', 'email', 'password', 'is_active',)}),
        ('Даты',
        {'fields': ('date_joined', 'last_login',)}),
        ('Разрешения',
        {'fields': ('is_staff', 'is_superuser',)}),
    )
    
    add_fieldsets = (
        ('Персональная информация',
        {'fields': ('username', 'email', 'password1', 'password2', 'is_active',)}),
        ('Даты',
        {'fields': ('date_joined', 'last_login',)}),
        ('Разрешения',
        {'fields': ('is_staff', 'is_superuser',)}),
    )