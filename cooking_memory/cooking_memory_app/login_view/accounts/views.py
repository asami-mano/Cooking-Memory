from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import(
    TemplateView,CreateView,FormView,View
)
from django.urls import reverse_lazy,reverse
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash,get_user_model
from .forms import RegistForm,UserLoginForm,UserLoginForm2,EmailChangeForm,PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib import messages
from django.utils.crypto import get_random_string
from .models import Invitation,ShareGroup,User
from django.http import JsonResponse,Http404
from django.views import View
from django.views.generic.edit import FormView

User = get_user_model()

class HomeView(TemplateView):
    template_name='home.html'
    
class RegistUserView(CreateView):
    template_name = 'regist.html'
    form_class = RegistForm
    success_url = reverse_lazy('cooking_records:my_list')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True
        user.save()

        # ここでログイン処理
        user = authenticate(self.request, email=user.email, password=form.cleaned_data['password'])
        if user is not None:
            login(self.request, user)
        else:
            print("認証失敗")
            
        return super().form_valid(form)
    
class UserLoginView2(FormView):
    template_name='user_login_2.html'
    form_class=UserLoginForm2
    success_url = reverse_lazy('cooking_records:my_list')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(self.request, email=email, password=password)
        if user:
            login(self.request, user)
            return super().form_valid(form)
        else:
            messages.error(self.request, "メールアドレスまたはパスワードが正しくありません。")
            return self.form_invalid(form)
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        print('next: ', next_url)
        return next_url if next_url else self.success_url

class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'user_logout.html')

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('cooking_records:my_list')
    
class UserLoginView(LoginView):
    template_name = 'user_login.html'
    next_page = reverse_lazy('accounts:home')
    form_class = UserLoginForm

class UserLogoutView2(LogoutView):
    next_page = reverse_lazy('cooking_records:my_list')
    http_method_names = ['get', 'post']
    template_name = 'user_logout.html'   
    
class UserView(LoginRequiredMixin, TemplateView):
    template_name = 'user.html'
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

class ChangeEmailView(LoginRequiredMixin,FormView):
    template_name='change_email.html'
    form_class=EmailChangeForm
    success_url = reverse_lazy('accounts:user')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request  # ←ここで渡す
        return kwargs
    
    def form_valid(self, form):
        user = self.request.user
        user.email = form.cleaned_data['new_email']
        user.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        print('next: ', next_url)
        return next_url if next_url else self.success_url

class MyPasswordChangeView(LoginRequiredMixin, FormView):
    template_name='change_password.html'
    form_class=PasswordChangeForm
    success_url = reverse_lazy('accounts:user')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # ←ここで渡す
        return kwargs
    
    def form_valid(self, form):
        new_password = form.cleaned_data['new_password']
        user = self.request.user
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(self.request, user)  # ← これでログアウトされないように！
        return super().form_valid(form)
    
class MyPageView(LoginRequiredMixin, TemplateView):
    template_name = 'mypage.html'
        
class GenerateInviteView(LoginRequiredMixin, TemplateView):
    template_name = 'generate_invite.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        token = get_random_string(20)
        
        # フルURLはcontextに渡すだけ
        invite_url = self.request.build_absolute_uri(
            reverse('accounts:share_regist', args=[token])
        )
        
        # invitation_urlにはtokenだけ保存
        Invitation.objects.create(
            user=self.request.user,
            invitation_url=token,
            used=0  # 0: 未使用
        )
            
        context['invite_url'] = invite_url
        return context
    
class InviteRegistUserView(CreateView):
    template_name = 'regist.html'
    form_class = RegistForm
    success_url = reverse_lazy('cooking_records:my_list')

    def dispatch(self, request, *args, **kwargs):
        self.invitation_url = kwargs.get('invitation_url')  # 招待URLの取得
        try:
            self.invitation = Invitation.objects.get(invitation_url=self.invitation_url, used=0)
        except Invitation.DoesNotExist:
            raise Http404("この招待URLは無効か、すでに使用されています。")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        # 招待者を取得
        inviter = self.invitation.user
        # 招待者がshare_groupを持っていなければ作成
        if not inviter.share_group:
            group = ShareGroup.objects.create()
            inviter.share_group = group
            inviter.save()
        else:
            group = inviter.share_group

        # 招待されたユーザーにもグループを割り当て
        user.share_group = group
        user.is_active = True
        user.save()

        # 招待トークンを使用済みにする
        self.invitation.used = 1
        self.invitation.save()

        # ここでログイン処理
        user = authenticate(self.request, email=user.email, password=form.cleaned_data['password'])
        if user is not None:
            login(self.request, user)
        else:
            print("認証失敗")
            
        return super().form_valid(form)

class ShareUsersView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            print("ログインユーザー：", request.user)
            print("ユーザーのグループ：", request.user.share_group)
            
            share_group = request.user.share_group
            
            if share_group is None:
                # 共有グループに属していなければ空リストを返す
                return JsonResponse({'users': []})
        
            users = User.objects.filter(share_group=share_group).exclude(id=request.user.id)
            
            print("共有中ユーザー：", users)
            
            data = {
                'users': [{'name': user.username} for user in users]
            }
        except Exception as e:
            print("エラー内容：", str(e))
            
            data = {
                'error': str(e)
            }

        return JsonResponse(data)
    
class UploadProfileImageView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        
        if 'image' in request.FILES:
            user.image_url = request.FILES['image']
            user.save()
        return redirect('accounts:mypage')
    
class ChangeUsernameView(LoginRequiredMixin, View):
    def post(self, request):
        new_username = request.POST.get('username')
        if new_username:
            request.user.username = new_username
            request.user.save()
        return redirect('accounts:mypage')