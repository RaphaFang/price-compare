from django.urls import path
from myapp import views
from myapp.weekly_task_api import api_upload

urlpatterns = [
    path('w1/', views.w1, name='w1'),
    path('/api/upload', api_upload.upload_task, name='api_upload'),
]