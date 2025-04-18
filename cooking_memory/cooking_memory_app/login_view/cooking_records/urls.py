from django.urls import path
from .views import(
    MyListView,
)

app_name='cooking_records'
urlpatterns = [
    path('my_list/',MyListView.as_view(),name='my_list'),

]