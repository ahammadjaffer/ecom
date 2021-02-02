from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.db import IntegrityError
from datetime import datetime
from ..models import *

def dashboard(request):
    context = {}
    return render(request, 'portal/admin/dashboard.html', context)

def admin_profile(request):
    if request.method == 'POST':
        try:
            portaluserid = request.user.id
            updateuser = User.objects.get(username=request.user)
            updateuser.email = request.POST['email']
            updateuser.profile.phonenumber = request.POST['phone']
            updateuser.save()
            messages.success(request, 'Saved Successfully')
            return redirect('/adminprofile/')
        except Exception as e:
            messages.error(request, 'Error: Profile update failed. Reason:- '+ str(e))
    profile = Profile.objects.filter(user_id=request.user.id)
    for p in profile:
        profiledata = p
    context = {'profiledata': profiledata}
    return render(request, 'portal/admin/profile.html', context)

def changepassword(request):
    profiledata=[]
    try:
        saveuser = User.objects.get(id=request.user.id)
        if saveuser.check_password(request.POST.get('password_old')):
            saveuser.set_password(request.POST['password_1'])
            saveuser.save()
            messages.success(request, 'Saved Successfully')
        else:
            messages.warning(request, 'Old password is incorrect')
        profile = Profile.objects.filter(user_id=request.user.id)
        for p in profile:
            profiledata = p
    except Exception as e:
        messages.error(request, 'Error: Password changing failed. Reason:- '+ str(e))
    context = {'profiledata': profiledata}
    return render(request, 'portal/admin/profile.html', context)

def adminlist(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'portal/admin/profilelist.html', context)

def productcategory(request):
    try:
        if request.method == 'POST':
            categoryname = request.POST['categoryname']
            obj = Category(name=categoryname,status=1)
            obj.save()
            messages.success(request, 'Saved Successfully')
    except Exception as e:
        messages.error(request, 'Error: Category not added. Reason:- '+ str(e))
    categories = Category.objects.filter(status=1)
    context = {'categories': categories}
    return render(request, 'portal/admin/productcategory.html', context)

def updatecategory(request):
    try:
        category = Category.objects.get(id=request.POST['categoryid'])
        category.name=request.POST['editcategoryname']
        category.save()
        messages.success(request, 'Category updated succesfully')
    except Exception as e:
        messages.error(request, 'Error: Category not updated. Reason:- '+ str(e))
    categories = Category.objects.filter(status=1)
    context = {'categories': categories}
    # return render(request, 'portal/admin/productcategory.html', context)
    return HttpResponseRedirect('/productcategory/')

def deletecategory(request):
    if request.method == 'GET':
        categoryid = request.GET['categoryid']
        try:
            category = Category.objects.get(id=categoryid)
            category.enddate=datetime.now()
            category.status=0
            category.save()
            messages.success(request, 'Category deleted succesfully')
        except Exception as e:
            messages.error(request, 'Error: Category not deleted. Reason:- '+ str(e))
        return JsonResponse({"categoryid": categoryid}, status=200)