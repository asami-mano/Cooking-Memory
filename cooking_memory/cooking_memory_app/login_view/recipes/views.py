from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Recipe
from .forms import RecipeForm

@login_required
def recipe_list(request):
    query = request.GET.get('q', '')
    recipes = Recipe.objects.filter(user=request.user)
    if query:
        recipes = recipes.filter(name__icontains=query)

    return render(request, 'recipes/recipe_list.html', {
        'recipes': recipes,
        'query': query
    })

@login_required
def add_recipe(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        url = request.POST.get('recipe_url')
        if name and url:
            Recipe.objects.create(name=name, recipe_url=url, user=request.user)
            return redirect('recipes:recipe_list')
    return render(request, 'recipes/add_recipe.html')
    
