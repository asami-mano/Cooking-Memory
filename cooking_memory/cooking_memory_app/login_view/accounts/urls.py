from django.contrib.auth.views import PasswordChangeView
from django.urls import path
from .views import(
    RegistUserView,HomeView,UserLoginView,
    UserLogoutView,UserView,UserLoginView2,
    UserLogoutView2,ChangeEmailView,MyPasswordChangeView
)

app_name='accounts'
urlpatterns = [
    path('home/',HomeView.as_view(),name='home'),
    path('regist/',RegistUserView.as_view(),name='regist'),
    path('user_login/',UserLoginView.as_view(),name='user_login'),
    path('user_logout/',UserLogoutView.as_view(),name='user_logout'),
    path('user/', UserView.as_view(), name='user'),
    path('user_login2/',UserLoginView2.as_view(),name='user_login_2'),
    path('user_logout2/',UserLogoutView2.as_view(),name='user_logout_2'),
    path('change_email/',ChangeEmailView.as_view(),name='change_email'),
    path('change_password/',MyPasswordChangeView.as_view(),name='change_password'),


]
