from django.shortcuts import render


# 這邊是掛靜態網站
def home(request):
    return render(request, 'pc_project/index.html')

def w1(request):
    return render(request, 'weekly_task/w1.html')

def loading_test(request):
    return render(request, 'loading_test.html')
