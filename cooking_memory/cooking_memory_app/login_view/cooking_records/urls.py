from django.urls import path
from .views import(
    MyListView,CookingRecordCreateView
)

app_name='cooking_records'
urlpatterns = [
    path('my_list/',MyListView.as_view(),name='my_list'),
    path('create/', CookingRecordCreateView.as_view(), name='cooking_record_create'),

]