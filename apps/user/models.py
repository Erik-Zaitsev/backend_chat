from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin


# Create your models here.
class CustomUserManager(BaseUserManager):
    '''Класс для описания модели Менеджера пользователей'''   
    use_in_migrate = True
    
    def create_user(self, email, username, password):
        if not email:
            raise ValueError('Обязательное поле "Почта"')
        if not username:
            raise ValueError('Обязательное поле "Никнейм"')
        if not password:
            raise ValueError('Обязательное поле "Пароль"')
      
        custom_user = self.model(email=self.normalize_email(email))
    
        custom_user.email = email
        custom_user.username = username
        custom_user.set_password(password)
        custom_user.is_staff = False
        custom_user.is_superuser = False
        custom_user.is_active = True
        custom_user.save(using=self._db)
        return custom_user
    

    def create_staffuser(self, email, username, password):
        if not email:
            raise ValueError('Обязательное поле "Почта"')
        if not username:
            raise ValueError('Обязательное поле "Никнейм"')
        if not password:
            raise ValueError('Обязательное поле "Пароль"')

        custom_user = self.model(email=self.normalize_email(email))
    
        custom_user.email = email
        custom_user.username = username
        custom_user.set_password(password)
        custom_user.is_staff = True
        custom_user.is_superuser = False
        custom_user.is_active = True
        custom_user.save(using=self._db)
        return custom_user
        
        
    def create_superuser(self, email, username, password):
        if not email:
            raise ValueError('Обязательное поле "Почта"')
        if not username:
            raise ValueError('Обязательное поле "Никнейм"')
        if not password:
            raise ValueError('Обязательное поле "Пароль"')
        
        custom_user = self.model(email=self.normalize_email(email))
    
        custom_user.email = email
        custom_user.username = username
        custom_user.set_password(password)
        custom_user.is_staff = True
        custom_user.is_superuser = True
        custom_user.is_active = True
        custom_user.save(using=self._db)
        return custom_user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    '''Класс для описания модели Пользователя'''
    
    REQUIRED_FIELDS = ['username', 'password',]
    USERNAME_FIELD = 'email'
    objects = CustomUserManager()
    
    username = models.CharField(verbose_name='Пользователь', max_length=50, unique=True)
    email = models.CharField(verbose_name='Почта', max_length=150, unique=True)
    date_joined = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='Последний вход', auto_now=True)
    is_staff = models.BooleanField(verbose_name='Администратор', default=False)
    is_superuser = models.BooleanField(verbose_name='Суперпользователь', default=False)
    is_active = models.BooleanField(verbose_name='В сети', default=True)
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        
    def __str__(self):
        return self.username