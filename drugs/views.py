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

def contact(request):
    return render(request, "contact.html")
def login(request):
    return render(request,"login.html")

def base(request):
    return render(request,"base.html")

def dealerdata(request):
    return render(request,"dealerinput.html")

def masterinput(request):
    return render(request,"masterinput.html")