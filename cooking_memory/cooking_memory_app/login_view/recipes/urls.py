from django.urls import path
from . import views

app_name='recipes'
urlpatterns = [
    path('recipe_list/',views.recipe_list,name='recipe_list'),
    path('add_recipe/',views.add_recipe,name='add_recipe'),

]