from django.urls import path
from .views import(
    MyListView,CookingRecordCreateView,toggle_favorite
)
from . import views

app_name='cooking_records'
urlpatterns = [
    path('my_list/',MyListView.as_view(),name='my_list'),
    path('create/', CookingRecordCreateView.as_view(), name='cooking_record_create'),
    path('create-category/', views.create_cooking_category, name='create_cooking_category'),
    path('<int:pk>/toggle_favorite/', toggle_favorite, name='toggle_favorite'),

]