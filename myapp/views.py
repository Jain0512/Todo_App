from django.shortcuts import render,redirect

from django.contrib.auth.models import User
from myapp import models
from myapp.models import TODOO
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def signup(request):
    if request.method == 'POST':
        fnm=request.POST.get('fnm')
        emailid=request.POST.get('emailid')
        pwd=request.POST.get('pwd')
        print(fnm,emailid,pwd)
        my_user=User.objects.create_user(fnm,emailid,pwd)
        my_user.save()
        return redirect('/Login')
    return render(request,"signup.html")

def loginn(request):
    if request.method == 'POST':
        fnm=request.POST.get("fnm")
        pwd=request.POST.get("pwd")
        print(fnm,pwd)
        user=authenticate(request,username=fnm,password=pwd)
        if user is not None:
            login(request,user)
            return redirect("/todopage")
        else:
            return redirect('/Login')

    return render(request,'loginn.html')

@login_required(login_url='/Login')
def todo(request):
    if request.method=='POST':
        title=request.POST.get("title")
        print(title)
        obj=models.TODOO(title=title,user=request.user)
        obj.save()
        res=models.TODOO.objects.filter(user=request.user).order_by("-date")
        return redirect('/todopage',{'res':res})
    res=models.TODOO.objects.filter(user=request.user).order_by("-date")
        
    return render(request,"todo.html",{'res':res})

@login_required(login_url='/Login')
def edit_todo(request,srno):
    if request.method=='POST':
        title=request.POST.get("title")
        print(title)
        obj=models.TODOO.objects.get(srno=srno)
        obj.title=title
        obj.save()
        return redirect("/todopage")
    obj=models.TODOO.objects.get(srno=srno)
        
    return render(request,"edit_todo.html",{'obj':obj})

@login_required(login_url='/Login')
def delete_todo(request,srno):
    print(srno)
    obj=models.TODOO.objects.get(srno=srno)
    obj.delete()
    return redirect('/todopage')

def signout(request):
    logout(request)
    return redirect('/Login')
