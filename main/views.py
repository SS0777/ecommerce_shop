from django.shortcuts import render

def home(request):
    return render(request, 'main/home.html')


def about(request):
    return render(request, 'main/about.html')

def terms(request):
    return render(request, 'main/terms.html')

def privacy(request):
    return render(request, 'main/privacy.html')