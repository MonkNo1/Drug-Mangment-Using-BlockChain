from django.shortcuts import render
from django.http import HttpResponse
from . import webs3
webs3.call_me_first()
password = {'prd':['monk',"monk123"],'mas' : ['abi','abi123'],'hos':['hari','hari123'],'buyd':['dhan','dhan123']}


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
    print("login check")
    if request.method== 'POST':
        print("method check")
        uname = request.POST['name']
        passw = request.POST['passw']
        print('uname : ' + uname)
        print('passw : ' + passw)
        if passw in password['prd']:
            return render(request,"dealerinput.html")
        elif passw in password["mas"]:
            return render(request,"masterinput.html")
        elif passw in password["hos"]:
            return render(request,"hospitalinput.html")
        elif passw in password["buyd"]:
            return render(request,"drugbuy.html")
        else:
            return render(request,"login.html")
    else:
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
        hospid=request.POST['hospid']
        patid=request.POST['patid']
        docid=request.POST['docid']
        print("ProductID" + hospid)
        print("patid" +patid)
        print("docid" + docid)
        context = {
            "hospid" : hospid,
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