"""
URL configuration for rohit_mobile_project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('rohit_mobile_project.api.urls')),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('products/', TemplateView.as_view(template_name='products.html'), name='products'),
    path('products/<int:product_id>/', TemplateView.as_view(template_name='product_detail.html'), name='product_detail'),
    path('admin-dashboard/', TemplateView.as_view(template_name='admin_dashboard.html'), name='admin_dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
