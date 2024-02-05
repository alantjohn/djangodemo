from django.shortcuts import render,redirect
from shop.models import Category,Product
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

def allcategories(request):
    product=Category.objects.all()
    return render(request,'category.html',{'product':product})

def productdetails(request,p):
    c=Category.objects.get(name=p)
    p=Product.objects.filter(category=c)
    return render(request, 'product.html', {'c':c,'p':p})


def details(request,p):
    p=Product.objects.get(name=p)
    return render(request, 'details.html', {'p': p})

def register(request):
    if(request.method=="POST"):
        u=request.POST['u']
        p=request.POST['p']
        cp=request.POST['cp']
        f=request.POST['f']
        l=request.POST['l']
        e=request.POST['e']

        if(p==cp):
            user=User.objects.create_user(username=u,password=p,first_name=f,last_name=l,email=e)
            user.save()
            return redirect('shop:category')
        else:
            return HttpResponse('Password not same')
    return render(request, 'register.html')

def user_login(request):
    if(request.method=="POST"):
        u = request.POST['u']
        p = request.POST['p']
        user=authenticate(username=u,password=p)
        if user:
            login(request,user)
            return redirect('shop:category')
        else:
            return HttpResponse('Invalid')
    return render(request,'login.html')

def user_logout(request):
    logout(request)
    return redirect('shop:category')