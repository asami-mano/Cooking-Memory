from django.urls import path
from .views import RecipeListView,RecipeCreateView

app_name='recipes'
urlpatterns = [
    path('recipe_list/',RecipeListView.as_view(),name='recipe_list'),
    path('add_recipe/',RecipeCreateView.as_view(),name='add_recipe'),

]