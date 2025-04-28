from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import(
    MyListView,CookingRecordCreateView,CreateCookingCategoryView,
    CreateToggleFavoriteView,CookingRecordDetailView,
    CookingRecordDeleteView,CookingRecordUpdateView,ToggleFavoriteView
)
from . import views

app_name='cooking_records'
urlpatterns = [
    path('my_list/',MyListView.as_view(),name='my_list'),
    path('create/', CookingRecordCreateView.as_view(), name='cooking_record_create'),
    path('create_category/', CreateCookingCategoryView.as_view(), name='create_cooking_category'),
    path('create_toggle_favorite/', CreateToggleFavoriteView.as_view(), name='create_toggle_favorite'),
    path('record_detail/<int:pk>/', CookingRecordDetailView.as_view(), name='record_detail'),
    path('cooking_record/<int:pk>/delete/', CookingRecordDeleteView.as_view(), name='cooking_record_delete'),
    path('<int:pk>/update/', CookingRecordUpdateView.as_view(), name='cooking_record_update'),
    path('<int:pk>/toggle_favorite/', ToggleFavoriteView.as_view(), name='toggle_favorite'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)