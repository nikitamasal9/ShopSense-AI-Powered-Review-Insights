from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.user_login, name='sign_in'),
    # path('signup/', views.sign_up, name='sign_up'),    
    path('onboarding/', views.onboarding, name='onboarding'),
    path('customer/signup/', views.customer_signup, name='customer_signup'),
    # path('search/', views.search, name='search'),
    # path('profile/', views.profile, name='profile'),
    # path('settings/', views.settings, name='settings'),
    path('logout/', views.user_logout, name='logout'),
    path('seller/signup/', views.seller_signup, name='seller_signup'),
]