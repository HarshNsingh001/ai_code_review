from django.urls import path
from . import views

urlpatterns = [
    path('review/', views.review_code, name='review_code'),
    path('reviews/', views.get_review_history, name='review_history'),
    path('review/<int:review_id>/', views.get_review_detail, name='review_detail'),
    path('health/', views.health_check, name='health_check'),
]