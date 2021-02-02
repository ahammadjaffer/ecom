from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .subviews import *

def home(request):
    context = {}
    if request.user.is_authenticated:
        if (request.user.is_superuser):
            return redirect('admin_home')
    return render(request, 'portal/home.html', context)

def register(request):
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
                print("Username or Password is incorrect")
                messages.info(request, 'Username or Password is incorrect')
        context={}
        return render(request, 'portal/register.html', context)

def user_logout(request):
    logout(request)
    return redirect('home')