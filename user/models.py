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
      
        CustomUser = self.model(email=self.normalize_email(email))
    
        CustomUser.email = email
        CustomUser.username = username
        CustomUser.set_password(password)
        CustomUser.is_staff = False
        CustomUser.is_superuser = False
        CustomUser.is_active = True
        CustomUser.save(using=self._db)
        return CustomUser
    

    def create_staffuser(self, email, username, password):
        if not email:
            raise ValueError('Обязательное поле "Почта"')
        if not username:
            raise ValueError('Обязательное поле "Никнейм"')
        if not password:
            raise ValueError('Обязательное поле "Пароль"')

        CustomUser = self.model(email=self.normalize_email(email))
    
        CustomUser.email = email
        CustomUser.username = username
        CustomUser.set_password(password)
        CustomUser.is_staff = True
        CustomUser.is_superuser = False
        CustomUser.is_active = True
        CustomUser.save(using=self._db)
        return CustomUser
        
        
    def create_superuser(self, email, username, password):
        if not email:
            raise ValueError('Обязательное поле "Почта"')
        if not username:
            raise ValueError('Обязательное поле "Никнейм"')
        if not password:
            raise ValueError('Обязательное поле "Пароль"')
        
        CustomUser = self.model(email=self.normalize_email(email))
    
        CustomUser.email = email
        CustomUser.username = username
        CustomUser.set_password(password)
        CustomUser.is_staff = True
        CustomUser.is_superuser = True
        CustomUser.is_active = True
        CustomUser.save(using=self._db)
        return CustomUser



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