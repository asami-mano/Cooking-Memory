from django.urls import path
from .views import(
    RecipeListView,
)

app_name='recipes'
urlpatterns = [
    path('recipe_list/',RecipeListView.as_view(),name='recipe_list'),

]