from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,AbstractUser,PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone


#https://docs.djangoproject.com/en/2.0/topics/auth/customizing/#django.contrib.auth.models.AbstractBaseUser 
#AbstractBaseUser model
# https://github.com/django/django/blob/master/django/contrib/auth/base_user.py
# base_user model


# https://github.com/django/django/blob/master/django/db/models/fields/__init__.py
# django.db.models

class MyUserManager(BaseUserManager):
# https://github.com/django/django/blob/master/django/contrib/auth/base_user.py#L16
# BaseUserManager
    use_in_migrations = True 
# TODO: WHY?  
# FIXME: If set to True the manager will be serialized into migrations and will
#        thus be available in e.g. RunPython operations.

    def _create_user(self,username,password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        username = self.normalize_email(username)    
        user = self.model(
            email=self.normalize_email(email),
            # normalize_email is a class method of BaseUserManager
            # Normalizes email addresses by lowercasing the domin portion of the eamil address
            # https://docs.djangoproject.com/en/2.0/topics/auth/customizing/#django.contrib.auth.models.BaseUserManager
        )    
        user = self.model(username=username, **extra_fields)

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_user(self, username,  password=None, **extra_fields):

        extra_fields.setdefault('is_staff', False)
# TODO: setdefualt()
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username,  password, **extra_fields):

        extra_fields.setdefault('is_staff', True)

        extra_fields.setdefault('is_superuser', True)



        if extra_fields.get('is_staff') is not True:

            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:

            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username,  password, **extra_fields)    

class MyUser(AbstractBaseUser,PermissionsMixin):
    # rebuild my own user model, all steps are the same as AbstractUser's
    # Making email address as username

    # https://github.com/django/django/blob/master/django/contrib/auth/models.py#L288
    # AbstractUser model   

    # https://github.com/django/django/blob/master/django/contrib/auth/base_user.py#L47
    # AbstractBaseUser

    username_validator = UnicodeUsernameValidator()

    username = models.EmailField(
        _('username'),
        max_length = 150,
        unique = True,
        help_text = _('Required valid email address'),
        validators = [username_validator],
        error_message = {
            'unique': _('A user with that emaill address already exist.'),
        },
    )


    is_staff = models.BooleanField(
        _('staff status'),
        defualt = False,
        help_text = _(
            'Designates whether the user can log into this admin site.'
        )
    )
    is_active = models.BooleanField(
        _('active'),
        defualt = True,
        help_text=_(

            'Designates whether this user should be treated as active. '

            'Unselect this instead of deleting accounts.'

        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    is_admin = models.BooleanField(default = False)
    
    object = MyUserManager()
    
    USERNAME_FIELD = 'username'

    class Meta:

        verbose_name = _('user')

        verbose_name_plural = _('users')
# AbstractBase methods


    


