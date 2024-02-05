from django.shortcuts import render
from shop.models import Product
from cart.models import Cart
from cart.models import Order
from cart.models import Account
from django.http import HttpResponse

def cartview(request):
    u = request.user  # current login user
    cart=Cart.objects.filter(user=u)
    total=0
    for i in cart:
        total+=i.quantity*i.product.price
    return render(request, 'cartview.html',{'c':cart,'total':total})
def addtocart(request,n):
    p=Product.objects.get(name=n)
    u=request.user
    try:
        cart=Cart.objects.get(user=u,product=p)
        if(cart.quantity < cart.product.stock):
            cart.quantity+= 1
            cart.save()
    except:
        if(p.stock > 0):
            cart = Cart.objects.create(product=p, user=u, quantity=1)
            cart.save()
    return cartview(request)

def cartminus(request,n):
    p=Product.objects.get(name=n)
    u=request.user
    try:
        cart=Cart.objects.get(user=u,product=p)
        if(cart.quantity >1):
            cart.quantity-= 1
            cart.save()
        else:
            cart.delete()
    except:
        pass
    return cartview(request)

def cartdelete(request,n):
    p = Product.objects.get(name=n)
    u = request.user

    cart = Cart.objects.get(user=u, product=p)
    cart.delete()

    return cartview(request)

def orderform(request):
    if(request.method=="POST"):
        a=request.POST['a']
        p=request.POST['p']
        n=request.POST['n']
        u=request.user
        cart=Cart.objects.filter(user=u)
        total = 0
        for i in cart:
            total += i.quantity * i.product.price
        try:
            num=int(n)
            ac=Account.objects.get(acctnum=num)
            if(ac.amount >= total):
                ac.amount=ac.amount-total
                ac.save()
                for i in cart:
                    o = Order.objects.create(user=u, product=i.product, address=a, phone=p, no_of_items=i.quantity,
                                             order_status="paid")
                    o.save()
                cart.delete()
                msg = "You order placed successfully"
                return render(request, 'orderdetails.html', {'msg': msg})

            else:
                msg = "Insufficient Amount. You can't place order"
                return render(request, 'orderdetails.html', {'msg': msg})

        except:
            pass

    return render(request, 'orderform.html')

def orderdetails(request):
    if (request.method == "POST"):
        u = request.user
        cart = Cart.objects.filter(user=u)
        for i in cart:
            o = Order.objects.create(user=u, product=i.product, address=a, phone=p, no_of_items=i.quantity,
                                     order_status="paid")
            o.save()
    return render(request, 'order.html',{'o':o,'u':u.username})







