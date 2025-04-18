from django.db import models
from django.contrib.auth.models import(
    BaseUserManager,AbstractBaseUser,PermissionsMixin
)
from django.urls import reverse_lazy
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self,username,email,password):
        if not email:
            raise ValueError('Emailを入力してください')
        if not password:
            raise ValueError('Passwordを入力してください')
        user=self.model(
            username=username,
            email=self.normalized_email(email)
        )
        user.set_password(password)
        user.save()
        return user

class User(AbstractBaseUser,PermissionsMixin):
    username=models.CharField(max_length=30)
    email=models.EmailField(max_length=100,unique=True)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    
    share_group_id = models.IntegerField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']
    
    objects=UserManager()
    
    def get_absolute_url(self):
        return reverse_lazy("accounts:home")#あとでhomeをmypageに変更する
    