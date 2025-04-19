from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import(
    TemplateView,
)

class MyListView(LoginRequiredMixin,TemplateView):
    template_name='my_list.html'
