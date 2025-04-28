from django.urls import path
from .views import(
    MyListView,CookingRecordCreateView,CookingRecordToggleFavoriteView,
    CookingRecordDetailView,CookingRecordDeleteView
)
from . import views

app_name='cooking_records'
urlpatterns = [
    path('my_list/',MyListView.as_view(),name='my_list'),
    path('create/', CookingRecordCreateView.as_view(), name='cooking_record_create'),
    path('create_category/', views.create_cooking_category, name='create_cooking_category'),
    path('<int:pk>/toggle_favorite/', CookingRecordToggleFavoriteView.as_view(), name='toggle_favorite'),
    path('record_detail/<int:pk>/', CookingRecordDetailView.as_view(), name='record_detail'),
    path('cooking_record/<int:pk>/delete/', CookingRecordDeleteView.as_view(), name='cooking_record_delete'),

]