from django.urls import path
from myapp import views
from myapp.weekly_task_api.api_upload import UploadTask
from myapp.weekly_task_api.api_download import DownloadTask


# 這個是處理/task的路由機制
urlpatterns = [
    path('', views.w1, name='w1'),
    # path('api/upload', api_upload.upload_task, name='api_upload'),

    path('api/upload', UploadTask.as_view(), name='upload_task'),
    path('api/download', DownloadTask.as_view(), name='download_task'),
]