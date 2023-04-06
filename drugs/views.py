from django.shortcuts import render
from django.http import HttpResponse
# from . import webs3


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

def prddata(request):
    if request.method=='POST':
        drg_id=request.POST['drgid']
        no_of_drg=request.POST['totdrg']
        print("drg id  :" + drg_id )
        print("no of drugs : " + no_of_drg)
        context = {
            "drgid" :  drg_id,
            "totdrg" : no_of_drg
         }
        return render(request,"temp.html",context)
    else:
        return render(request,"dealerinput.html")

def masterinput(request):
    if request.method=='POST':
        ProductID=request.POST['PrdID']
        avilamt=request.POST['avilamt']
        thres=request.POST['thres']
        PripU=request.POST['PripU']
        print("ProductID" +  ProductID)
        print("avilamt" + avilamt)
        print("thres" + thres)
        print("PripU" + PripU)
        context = {
            "ProductID" :  ProductID,
            "avilamt" : avilamt,
            "thres" : thres,
            "PripU" : PripU
         }
        return render(request,"temp.html",context)
    else:
        return render(request,"masterinput.html")

def hostpitalinput(request):
    if request.method=='POST':
        ProductID=request.POST['ProductID']
        patid=request.POST['patid']
        docid=request.POST['docid']
        print("ProductID" + ProductID)
        print("patid" +patid)
        print("docid" + docid)
        context = {
            "ProductID" : ProductID,
            "patid" :patid,
            "docid" : docid
         }
        return render(request,"temp.html",context)
    else:
        return render(request,"hospitalinput.html")

def drugbuy(request):
    if request.method=='POST':
        hosid=request.POST['hosid']
        ProductID=request.POST['ProductID']
        patid=request.POST['patid']
        docid=request.POST['docid']
        reqamt=request.POST['reqamt']
        print("hosid" +  hosid)
        print("ProductID" + ProductID)
        print("patid" + patid)
        print("docid" + docid)
        print("reqamt" + reqamt)
        context = {
            "hosid" :  hosid,
            "ProductID" : ProductID,
            "patid" : patid,
            "docid" :docid,
            "reqamt" : reqamt
         }
        return render(request,"temp.html",context)
    else:
        return render(request,"drugbuy.html")