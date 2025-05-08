
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from login_view.views import PortfolioView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', PortfolioView.as_view(), name='portfolio'),  # ← トップページに設定
    path('accounts/', include('accounts.urls')),
    path('cooking_records/', include('cooking_records.urls')),
    path('recipes/', include('recipes.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)