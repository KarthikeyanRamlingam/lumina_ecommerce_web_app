from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from store import views
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'categories', views.CategoryViewSet)

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/register/', views.register),
    path('api/auth/login/', views.user_login),
    path('api/auth/logout/', views.user_logout),
    path('api/auth/me/', views.current_user),
    path('api/orders/', views.place_order),
    path('api/orders/my/', views.my_orders),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
