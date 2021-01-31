from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def viewallproducts(request):
    context = {}
    return render(request, 'portal/viewallproducts.html', context)