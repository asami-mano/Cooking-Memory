from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import(
    TemplateView,
)

class RecipeListView(LoginRequiredMixin,TemplateView):
    template_name='recipe_list.html'
