from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self,email,username,password = None):
        if not email:
            raise ValueError("Email Required")
        if not username:
            raise ValueError("Username required")

        user = self.model(
            email = self.normalize_email(email),
            username = username, 
            )

        user.set_password(password)
        user.save(using = self._db)
        return user

    # creating a super user (admin)
    def create_superuser(self,email,username,password):
        user = self.create_user(
            email = self.normalize_email(email),
            password = password,
            username = username,
            )
        user.is_prospect = False 
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True 
        user.is_coach = True 
        user.save(using = self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name = ('email'), max_length = 60, unique = True)
    username = models.CharField(max_length = 30, unique = True)
    date_joined = models.DateTimeField(verbose_name = 'date joined', auto_now_add = True)
    last_login = models.DateTimeField(verbose_name = 'last login',auto_now = True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)

   # OUTFRNT permissions
    is_coach = models.BooleanField(default = False)
    is_client = models.BooleanField(default = False)
    is_newclient = models.BooleanField(default = False) 
    is_prospect = models.BooleanField(default = True)

    objects = UserManager()

    # onboarding fields 
    
    # completed Sales & Marketing questions
    completed_P1 = models.BooleanField(default = False)
    # completed People & Culture questions
    completed_P2 = models.BooleanField(default = False)
    # completed Accounting & Finance questions
    completed_P3 = models.BooleanField(default = False)
    # completed Business & Operations questions
    completed_P4 = models.BooleanField(default = False)
    # completed Legal & Governance questions
    completed_P5 = models.BooleanField(default = False)
    # completed Technology questions
    completed_P6 = models.BooleanField(default = False)
    
    # completed questionnaire 
    categories_answered = models.IntegerField(default = 0)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # display user information 
    def __str__(self):
       return self.username

    def has_perm(self,perm,obj = None):
        return self.is_admin
    
    def has_module_perms(self,app_label):
        return True
