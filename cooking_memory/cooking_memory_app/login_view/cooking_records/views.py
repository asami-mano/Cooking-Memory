from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import(
    ListView,CreateView,DetailView,DeleteView,UpdateView
)
from django.urls import reverse_lazy
from .models import CookingRecord,CookingCategory,CookingRecordRecipe,Recipe
from .forms import CookingRecordForm
import json


class MyListView(LoginRequiredMixin, ListView):
    model = CookingRecord
    template_name = 'cooking_records/my_list.html'
    context_object_name = 'cooking_records'

    def get_queryset(self):
        return CookingRecord.objects.filter(user=self.request.user).order_by('-date')
    
class CookingRecordCreateView(LoginRequiredMixin, CreateView):
    model = CookingRecord
    form_class = CookingRecordForm
    template_name = 'cooking_records/record_form.html'
    success_url = reverse_lazy('cooking_records:my_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipes'] = Recipe.objects.filter(user=self.request.user)
        return context

    def form_valid(self, form):
        print(self.request.POST)
        form.instance.user = self.request.user  # ユーザーを紐づける
        
        # hidden inputから is_favorite も取得してセット
        is_favorite = self.request.POST.get('is_favorite', '0')
        form.instance.is_favorite = int(is_favorite)
        
        response = super().form_valid(form)

        # hidden input からレシピIDを取得
        recipe_ids = self.request.POST.getlist('recipes')
        for rid in recipe_ids:
            if rid:  # 念のため空チェック
                CookingRecordRecipe.objects.create(
                    cooking_record=self.object,  # 作ったばかりのレコード
                    recipe_id=rid
                )
        return response
    
class CreateToggleFavoriteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
            try:
                # リクエストボディの取得
                data = json.loads(request.body)

                # レコードIDとお気に入り状態の取得
                record_id = data.get('record_id')
                is_favorite = data.get('is_favorite')
                
                if record_id is None or is_favorite is None:
                    return JsonResponse({'error': 'Invalid data'}, status=400)
                
                record = CookingRecord.objects.get(id=record_id, user=request.user)
                record.is_favorite = is_favorite
                record.save()
                
                return JsonResponse({'is_favorite': record.is_favorite})
            
            except CookingRecord.DoesNotExist:
                return JsonResponse({'error': 'Record not found'}, status=404)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid request'}, status=400)
    
class CreateCookingCategoryView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        name = data.get("name")
        if name:
            category = CookingCategory.objects.create(user=request.user, name=name)
            return JsonResponse({"success": True, "id": category.id, "name": category.name})
        return JsonResponse({"success": False}, status=400)
        
class CookingRecordDetailView(DetailView):
    model = CookingRecord
    template_name = 'cooking_records/record_detail.html'
    context_object_name = 'record'# テンプレートで使う変数名（record）
    
class CookingRecordDeleteView(DeleteView):
    model = CookingRecord
    template_name = 'cooking_record_confirm_delete.html'  # 使わないけど書く
    success_url = reverse_lazy('cooking_records:my_list')
    
class CookingRecordUpdateView(LoginRequiredMixin, UpdateView):
    model = CookingRecord
    form_class = CookingRecordForm
    template_name = 'cooking_records/record_update_form.html'
    success_url = reverse_lazy('cooking_records:my_list')

    def get_form_kwargs(self):
            kwargs = super().get_form_kwargs()
            kwargs['user'] = self.request.user
            return kwargs
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipes'] = Recipe.objects.filter(user=self.request.user)
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)

        # いったん既存の関連を全部削除
        self.object.cooking_record_recipes.all().delete()

        # 新しく選んだレシピを登録
        recipe_ids = form.cleaned_data['recipes']
        for recipe in recipe_ids:
            CookingRecordRecipe.objects.create(
                cooking_record=self.object,
                recipe=recipe
            )
        return response
    
class ToggleFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        record = get_object_or_404(CookingRecord, pk=pk, user=request.user)
        record.is_favorite = not record.is_favorite  # 現在の値を反転
        record.save()
        return JsonResponse({'is_favorite': record.is_favorite})
