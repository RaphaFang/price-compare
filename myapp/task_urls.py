from django.urls import path
from myapp import views
from myapp.weekly_task_api import api_upload, api_download

# 這個是處理/task的路由機制
urlpatterns = [
    path('', views.w1, name='w1'),
    path('api/upload', api_upload.upload_task, name='api_upload'),
    path('api/download', api_download.download_task, name='api_download'),
]