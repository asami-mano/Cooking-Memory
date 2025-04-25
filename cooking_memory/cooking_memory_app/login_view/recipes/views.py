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
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            return redirect('recipe_list')
    else:
        form = RecipeForm()
    
    return render(request, 'recipes/add_recipe.html', {'form': form})