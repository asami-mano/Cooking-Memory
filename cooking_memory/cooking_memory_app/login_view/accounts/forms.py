from django import forms
from .models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
import re

User = get_user_model()

class RegistForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput(),label='パスワード再入力')
    
    class Meta:
        model=User
        fields=['username','email','password']
        widgets={
            'password':forms.PasswordInput()
        }
        labels={
            'username':'名前/ニックネーム',
            'email':'メールアドレス',
            'password':'パスワード',
        }
        
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise ValidationError("パスワードは6文字以上で入力してください。")
        if not re.match(r'^[a-zA-Z0-9]+$', password):
            raise ValidationError("パスワードは英数字のみを使用してください。")
        return password
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("パスワードが一致しません。")
        return cleaned_data

    def save(self,commit=False):
        user=super().save(commit=False)
        validate_password(self.cleaned_data['password'],user)
        user.set_password(self.cleaned_data['password'])
        # user.save()
        return user
    
    
class UserLoginForm(forms.Form):
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())


class UserLoginForm2(forms.Form):
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())

class EmailChangeForm(forms.Form):
    email = forms.EmailField(label='現在のメールアドレス')
    new_email = forms.EmailField(label='新しいメールアドレス')
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # ←ここで取り出す
        super().__init__(*args, **kwargs)
    
class PasswordChangeForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(),label='現在のパスワード')
    new_password = forms.CharField(widget=forms.PasswordInput(),label='新しいパスワード')
    new_password2 = forms.CharField(widget=forms.PasswordInput(),label='新しいパスワード再入力')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # ←ここで取り出す
        super().__init__(*args, **kwargs)
        
    def clean(self):
        cleaned_data = super().clean()
        old = cleaned_data.get('password')
        new1 = cleaned_data.get('new_password')
        new2 = cleaned_data.get('new_password2')

        if not self.user.check_password(old):
            self.add_error('password', '現在のパスワードが違います')

        if new1 and new2 and new1 != new2:
            self.add_error('new_password2', 'パスワードが一致しません')

        return cleaned_data