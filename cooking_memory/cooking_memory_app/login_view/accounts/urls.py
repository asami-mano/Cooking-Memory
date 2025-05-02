from django.urls import path
from .views import(
    RegistUserView,HomeView,UserLoginView,
    UserLogoutView,UserView,UserLoginView2,
    UserLogoutView2,ChangeEmailView,MyPasswordChangeView,
    MyPageView,GenerateInviteView,InviteRegistUserView,
    ShareUsersView,UploadProfileImageView, ChangeUsernameView,
    
)
from django.conf import settings
from django.conf.urls.static import static

app_name='accounts'
urlpatterns = [
    # path('home/',HomeView.as_view(),name='home'),
    path('regist/',RegistUserView.as_view(),name='regist'),
    path('user_login/',UserLoginView.as_view(),name='user_login'),
    path('user_logout/',UserLogoutView.as_view(),name='user_logout'),
    path('user/', UserView.as_view(), name='user'),
    path('user_login2/',UserLoginView2.as_view(),name='user_login_2'),
    path('user_logout2/',UserLogoutView2.as_view(),name='user_logout_2'),
    path('change_email/',ChangeEmailView.as_view(),name='change_email'),
    path('change_password/',MyPasswordChangeView.as_view(),name='change_password'),
    path('mypage/', MyPageView.as_view(), name='mypage'),
    path('generate_invite/',GenerateInviteView.as_view(),name='generate_invite'),
    path('share_regist/<str:invitation_url>/', InviteRegistUserView.as_view(), name='share_regist'),
    path('share_users/', ShareUsersView.as_view(), name='share_users'),
    path('upload_profile_image/', UploadProfileImageView.as_view(), name='upload_profile_image'),
    path('change_username/', ChangeUsernameView.as_view(), name='change_username'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)