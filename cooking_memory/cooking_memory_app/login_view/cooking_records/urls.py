from django.urls import path
from .views import(
    MyListView,CookingRecordCreateView
)
from . import views

app_name='cooking_records'
urlpatterns = [
    path('my_list/',MyListView.as_view(),name='my_list'),
    path('create/', CookingRecordCreateView.as_view(), name='cooking_record_create'),
    path('create-category/', views.create_cooking_category, name='create_cooking_category'),

]