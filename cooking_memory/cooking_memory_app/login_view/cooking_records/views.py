from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import(
    ListView,
)
from .models import CookingRecord

class MyListView(LoginRequiredMixin, ListView):
    model = CookingRecord
    template_name = 'my_list.html'
    context_object_name = 'cooking_records'

    def get_queryset(self):
        return CookingRecord.objects.filter(user=self.request.user).order_by('-date')