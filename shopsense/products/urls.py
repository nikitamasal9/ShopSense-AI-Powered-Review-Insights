from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    # path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('update/<int:product_id>/', views.update_product, name='update_product'),
    path('subscribe/', views.subscribe, name='subscribe'), 
    # path('customer_reviews/', views.customer_reviews, name='customer_reviews'), 
    path('add/', views.add_product, name='add_product'),
    path('detail/<int:pk>/', views.product_detail, name='product_detail'),
    path('my-products/', views.seller_products, name='seller_products'),
    path('orders/', views.seller_orders, name='seller_orders'),
    path('orders/update/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('product/<int:product_id>/add-review/', views.add_review, name='add_review'),
]