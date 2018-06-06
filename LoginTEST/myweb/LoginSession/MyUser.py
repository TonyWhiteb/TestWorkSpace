from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self,email,password = None):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )    
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password):
        user = self.create_user(
            email,
            password = password
        )    
        user.is_admin = True
        user.save(using=self._db)
        return user
class MyUser(AbstractBaseUser):
    email = models.EmailField(verbose_name = 'email_add', max_length = 255, unique = True)
    password = models.TextField(verbose_name= 'password', max_length = 255)
    is_admin = models.BooleanField(default = False)
    object = MyUserManager()
    
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self,perm,obj = None):
        return True

    def has_module_perms(self,app_label):
        return True
    
