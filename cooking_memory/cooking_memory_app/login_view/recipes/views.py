from django.shortcuts import render
from django.views.generic import(
    TemplateView,
)

class RecipeListView(TemplateView):
    template_name='recipe_list.html'
