from django.urls import path
from myapp import views
from myapp.commerce_api.api_ebay import account_deletion_notification

# 這個是處理/pc的路由機制
urlpatterns = [
    path('', views.home, name='home'),
    path('ebay/deletion/', account_deletion_notification, name='account_deletion_notification'),


]
