from django.urls import path
from . import views
from shopsense.views import add_to_cart ,get_cart

urlpatterns = [
    path('add/', views.add_product, name='add_product'),
    path('', views.product_list, name='product_list'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('update/<int:product_id>/', views.update_product, name='update_product'),
    path('add/', views.add_product, name='add_product'),
    path("add-to-cart/", add_to_cart, name="add-to-cart"),
    path("get-cart/", get_cart, name="get-cart"),

]