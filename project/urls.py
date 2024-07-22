from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# project 是直接全局控制，所以是要引入我在myapp的檔案
urlpatterns = [
    path('admin/', admin.site.urls),
    path('pc/v1/', include('myapp.pc_urls')),
    path('task/v1/', include('myapp.task_urls')),
]

# 掛載css js的位置，不會與admin衝突
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)