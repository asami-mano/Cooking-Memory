from django.shortcuts import render
from django.views.generic import(
    TemplateView,
)

class MyListView(TemplateView):
    template_name='my_list.html'
