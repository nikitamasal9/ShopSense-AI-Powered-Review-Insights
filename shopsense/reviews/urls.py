from django.urls import path
from .views import ReviewAnalysis

urlpatterns = [
    path('api/analyze_review/', ReviewAnalysis.as_view(), name='analyze_review'),
]