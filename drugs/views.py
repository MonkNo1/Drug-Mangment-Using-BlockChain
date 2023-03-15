from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, "index.html")

def blog(request):
    return render(request, "blog.html")

def blogsingle(request):
    return render(request, "blog-single.html")

def features(request):
    return render(request, "features.html")

def pricing(request):
    return render(request, "pricing.html")
