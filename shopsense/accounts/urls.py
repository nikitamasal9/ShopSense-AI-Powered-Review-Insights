from django.urls import path
from . import views
from .views import UserListAPI

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('customer-login/', views.customer_login, name='customer_login'),
    path('seller-login/', views.seller_login, name='seller_login'),

    path('api/users/', UserListAPI.as_view(), name='api_users'),

]