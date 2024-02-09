from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, CustomUserManager


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):  
    list_display = [
        'username',
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
        {'fields': ('username', 'password',)}),
        ('Даты',
        {'fields': ('date_joined', 'last_login',)}),
        ('Разрешения',
        {'fields': ('is_staff', 'is_superuser',)}),
    )
    
    add_fieldsets = (
        ('Персональная информация',
        {'fields': ('username', 'password1', 'password2',)}),
        ('Даты',
        {'fields': ('date_joined', 'last_login',)}),
        ('Разрешения',
        {'fields': ('is_staff', 'is_superuser',)}),
    )