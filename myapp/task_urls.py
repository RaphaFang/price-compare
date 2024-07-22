from django.urls import path
from . import views
from weekly_task_api import api_upload

urlpatterns = [
    path('w1/', views.w1, name='w1'),
    path('/api/upload', api_upload, name='api_upload'),
]