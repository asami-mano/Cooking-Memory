from django.db import models
from django.contrib.auth.models import(
    BaseUserManager,AbstractBaseUser,PermissionsMixin
)
from django.urls import reverse_lazy
from django.utils import timezone
from django.conf import settings

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

class ShareGroup(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class User(AbstractBaseUser,PermissionsMixin):
    username=models.CharField(max_length=30)
    email=models.EmailField(max_length=100,unique=True)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    share_group = models.ForeignKey(ShareGroup, on_delete=models.SET_NULL, null=True, blank=True)
    image_url = models.ImageField(max_length=300,upload_to='profile_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']
    
    objects=UserManager()
    
    def get_absolute_url(self):
        return reverse_lazy("accounts:mypage")
    
class Invitation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    invitation_url = models.CharField(max_length=300, unique=True)
    used = models.IntegerField(default=0)# 0: 未使用, 1: 使用済み
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def is_used(self):
        return self.used == 1

