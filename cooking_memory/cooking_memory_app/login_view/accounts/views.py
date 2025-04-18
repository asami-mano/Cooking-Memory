from django.shortcuts import render,redirect
from django.views.generic import(
    TemplateView,CreateView,FormView,View
)
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from .forms import RegistForm,UserLoginForm,UserLoginForm2,EmailChangeForm,PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib import messages

class HomeView(TemplateView):
    template_name='home.html'
    
class RegistUserView(CreateView):
    template_name='regist.html'
    form_class=RegistForm
    success_url=reverse_lazy('accounts:home')
    
class UserLoginView2(FormView):
    template_name='user_login_2.html'
    form_class=UserLoginForm2
    success_url = reverse_lazy('accounts:user')

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
        return redirect('accounts:home')
    
class UserLoginView(LoginView):
    template_name = 'user_login.html'
    next_page = reverse_lazy('accounts:home')
    form_class = UserLoginForm

class UserLogoutView2(LogoutView):
    next_page = reverse_lazy('accounts:home')
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
    
    # def get_success_url(self):
    #     next_url = self.request.GET.get('next')
    #     print('next: ', next_url)
    #     return next_url if next_url else self.success_url

class MyPageView(LoginRequiredMixin, TemplateView):
    template_name = 'mypage.html'
    
class GenerateInviteView(LoginRequiredMixin, TemplateView):
    template_name = 'generate_invite.html'
    
class ShareUserView(LoginRequiredMixin, TemplateView):
    template_name = 'share_user.html'
