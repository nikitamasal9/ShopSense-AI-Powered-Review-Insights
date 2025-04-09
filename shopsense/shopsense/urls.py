"""
URL configuration for shopsense project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
# from django.urls import include, path
# from .views import home, product_detail, landing_page
from django.views.generic import RedirectView

urlpatterns = [
    # path('', landing_page, name='landing_page'),
    # path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls')),

    # path('product/<str:product_name>/', product_detail, name='product_detail'),  
    # path('admin/', admin.site.urls),
    # path("__reload__/", include("django_browser_reload.urls")),
    # path('seller_products/', include('products.urls')),  
    # path('reviews/', include('reviews.urls')),   
    # path('accounts/', include('accounts.urls')),  
    path('cart/', include('cart.urls')),
    path('', RedirectView.as_view(url='products/', permanent=True)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
