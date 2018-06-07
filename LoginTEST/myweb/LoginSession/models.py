from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,AbstractUser,PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator


#https://docs.djangoproject.com/en/2.0/topics/auth/customizing/#django.contrib.auth.models.AbstractBaseUser 
#AbstractBaseUser model
# https://github.com/django/django/blob/master/django/contrib/auth/base_user.py
# base_user model

# https://github.com/django/django/blob/master/django/contrib/auth/models.py#L288
# AbstractUser model
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
class MyUser(AbstractBaseUser,PermissionsMixin):
    # rebuild my own user model, all steps are the same as AbstractUser's
    # Making email address as username

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
    
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self,perm,obj = None):
        return True

    def has_module_perms(self,app_label):
        return True
    


