from django.urls import path
from . import views

urlpatterns = [
    path('w1/', views.w1, name='w1'),
]