from django.shortcuts import render

def home(request):
    return render(request, 'pc_project/index.html')

def w1(request):
    return render(request, 'weekly_task/w1.html')