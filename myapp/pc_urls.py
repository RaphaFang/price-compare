from django.urls import path
from . import views

# 這個是處理/pc的路由機制
urlpatterns = [
    path('', views.home, name='home'),
]
