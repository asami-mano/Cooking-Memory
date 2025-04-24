from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import(
    ListView,CreateView,
)
from django.urls import reverse_lazy
from .models import CookingRecord,CookingCategory
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
    success_url = reverse_lazy('cooking_records:my_list')  # マイリスト画面へ

    def form_valid(self, form):
        form.instance.user = self.request.user  # ユーザーを紐づける
        return super().form_valid(form)
    
@csrf_exempt
def create_cooking_category(request):
    if request.method == "POST" and request.user.is_authenticated:
        data = json.loads(request.body)
        name = data.get("name")
        if name:
            category = CookingCategory.objects.create(user=request.user, name=name)
            return JsonResponse({"success": True, "id": category.id, "name": category.name})
    return JsonResponse({"success": False})
