from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .subviews import *
from .subviews import portalview
from .models import *

from django.db import DatabaseError, transaction

def home(request):
    context = {}
    data = {}
    if request.user.is_authenticated:
        if (request.user.is_superuser):
            return redirect('dashboard')
    data['banners'] = Banners.objects.all()
    productlist = portalview.getproductsforhomepage(request)
    data['mobilelist'] = productlist[11]
    data['laptoplist'] = productlist[12]
    data['accessorylist'] = productlist[13]
    context = {'details':data}
    return render(request, 'portal/home.html', context)

def register(request):
    validation = []
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('newpassword')
        if User.objects.filter(username=email).exists():
            validation.append("Username already exists. Try different email.")
        if User.objects.filter(email=email).exists() and not(validation):
            validation.append("Email already exists. Try different email.")
        try:
            if not(validation):
                with transaction.atomic():
                    userobj = User.objects.create_user(first_name=firstname,
                    last_name=lastname,
                    username=email,
                    email=email,
                    password=password)
                    p = Profile.objects.get(user=userobj)
                    p.phonenumber = phone
                    p.save()
                    messages.success(request, 'Account created succesfully')
                    user = authenticate(request, username=email, password=password)
                    if user is not None:
                        login(request, user)
                        if (user.is_superuser):
                            return redirect('dashboard')
                        else:
                            return redirect('home')
                    else:
                        messages.info(request, 'Username or Password is incorrect')
            else:
                messages.info(request, validation[0])
        except Exception as e:
            messages.error(request, 'Error: '+ str(e))
    context = {}
    return render(request, 'portal/register.html', context)

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if (user.is_superuser):
                    return redirect('dashboard')
                else:
                    return redirect('home')
            else:
                messages.info(request, 'Username or Password is incorrect')
        context={}
        return render(request, 'portal/register.html', context)

def user_logout(request):
    logout(request)
    return redirect('home')