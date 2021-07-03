from django.db import reset_queries
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import OrderModel, PizzaModel, customermodel
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def home(request):
    return render(request, 'app1/home.html')

def adminlogin(request):
    return render(request,'app1/adminlogin.html')

def user_authenticate(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username = username, password = password)

    if user is not None and user.username=="swapfm":
        login(request,user)
        return redirect("adminhomepage")
    else:
        messages.add_message(request,messages.ERROR,"Invalid Credentials")
        return redirect('adminloginpage')
    
def adminhomepage(request):
    if not request.user.is_authenticated:
        return redirect('/')

    context = {'selected_pizzas': PizzaModel.objects.all()}
    return render(request,'app1/adminhome.html', context)

def user_logout(request):
    logout(request)
    return redirect("adminloginpage")

def addpizza(request):
    if not request.user.is_authenticated:
        return redirect('/')

    name = request.POST['pizza']
    price = request.POST['price']

    PizzaModel(name = name, price = price).save()
    return redirect('adminhomepage')

def deletepizza(request, pizzapk):
    PizzaModel.objects.filter(id = pizzapk).delete()
    return redirect('adminhomepage')


def signup(request):
    username = request.POST['username']
    password = request.POST['password']
    phone = request.POST['phone']
    mail = request.POST['email']

    if User.objects.filter(username = username).exists():
        messages.add_message(request, messages.ERROR, "User already exists")
        return redirect("home")
    User.objects.create_user(username = username, password = password).save()
    lastobj = len(User.objects.all())-1
    customermodel(userid = User.objects.all()[int(lastobj)].id, phone = phone).save()
    customermodel(userid = User.objects.all()[int(lastobj)].id, usermail = mail).save()
    messages.add_message(request, messages.ERROR, 'User Account Created')
    return redirect('home')

def userlogin(request):
    return render(request,"app1/userlogin.html")


def authenticate_user(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username = username, password = password)

    if user is not None:
        login(request, user)
        return redirect('/customerpage/')

    else:
        messages.add_message(request, messages.ERROR,"Invalid Username or Password")
        return redirect("/loginuser/")


def customerwelcome(request):
    if not request.user.is_authenticated:
        return redirect('/loginuser/')

    username = request.user.username
    context = {'username': username,'pizzas': PizzaModel.objects.all()}
    return render(request,'app1/customerhome.html',context)

def userlogout(request):
    if not request.user.is_authenticated:
        return redirect('/loginuser/')

    logout(request)
    return redirect('/loginuser/')

def placeorder(request):
    if not request.user.is_authenticated:
        return redirect('/loginuser/')

    username = request.user.username
    phoneno = customermodel.objects.filter(userid = request.user.id)[0].phone
    mail = customermodel.objects.filter(userid = request.user.id)[0].usermail
    print(mail)
    
    
    address = request.POST['address']
    order = ""

    for pizza in PizzaModel.objects.all():
        pizzaid = pizza.id
        name = pizza.name
        price = pizza.price
        
        quantity = request.POST.get(str(pizzaid)," ")
       
        if str(quantity)!="0" and str(quantity)!=" ":
             order = order+  name+ "price: " + str(int(price)*(int(quantity))) + " quantity : "+ quantity+ "  "
    
    subject = 'Pizza Order Confirmation'
    message = f'Hi {username}, Your Order has been successfully placed. We will deliver your delicious pizza soon.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [mail, ]
    send_mail( subject, message, email_from, recipient_list )
        
    print(order)
       

    OrderModel(username = username, phoneno = phoneno , address = address, ordereditems = order).save()
    messages.add_message(request, messages.ERROR, "Order Placed")
    return redirect('/customerpage/')

def userorders(request):
    orders = OrderModel.objects.filter(username = request.user.username)
    context = {'orders' : orders}
    return render(request,'app1/userorders.html', context)


def adminorders(request):
    orders = OrderModel.objects.all()
    context = {"orders" : orders}
    return render(request, 'app1/adminorders.html', context)

def acceptorder(request, orderpk):
    order = OrderModel.objects.filter(id = orderpk)[0]
    order.status = "Accepted"
    order.save()
    return redirect(request.META['HTTP_REFERER'])

def declineorder(request, orderpk):
     order = OrderModel.objects.filter(id = orderpk)[0]
     order.status = "Declined"
     order.save()
     return redirect(request.META['HTTP_REFERER'])