from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime
from portal.models import *

@login_required(login_url='user_login')
def customeraccount(request):
    context = {}
    userdetails = {}
    data={}
    user = request.user
    userdetails['firstname'] = user.first_name
    userdetails['lastname'] = user.last_name
    userdetails['email'] = user.email
    clientdetail = User.objects.filter(id=user.id)[0]
    userdetails['phone'] = clientdetail.profile.phonenumber
    userdetails['housename'] = '' if(clientdetail.profile.housename =='') else clientdetail.profile.housename
    userdetails['street'] = '' if(clientdetail.profile.street =='') else clientdetail.profile.street
    userdetails['landmark'] = '' if(clientdetail.profile.landmark =='') else clientdetail.profile.landmark
    userdetails['pincode'] = clientdetail.profile.pincode
    data['userdetails'] = userdetails
    context={'data':data}
    return render(request, 'portal/customeraccount.html', context)

@login_required(login_url='user_login')
def changecustomerpassword(request):
    profiledata=[]
    try:
        saveuser = User.objects.get(id=request.user.id)
        if saveuser.check_password(request.POST.get('password_old')):
            saveuser.set_password(request.POST['password_1'])
            saveuser.save()
            messages.success(request, 'Saved Successfully')
        else:
            messages.error(request, 'Old password is incorrect')
        profile = Profile.objects.filter(user_id=request.user.id)
        for p in profile:
            profiledata = p
    except Exception as e:
        messages.error(request, 'Error: Password changing failed. Reason:- '+ str(e))
    context = {'profiledata': profiledata}
    return redirect('/customeraccount')

@login_required(login_url='user_login')
def changecustomerdetails(request):
    profiledata=[]
    try:
        portaluserid = request.user.id
        updateuser = User.objects.get(username=request.user)
        updateuser.first_name = request.POST['firstname']
        updateuser.last_name = request.POST['lastname']
        updateuser.email = request.POST['email']
        updateuser.profile.housename = request.POST['house']
        updateuser.profile.street = request.POST['street']
        updateuser.profile.landmark = request.POST['landmark']
        updateuser.profile.state = request.POST['state']
        updateuser.profile.country = request.POST['country']
        updateuser.profile.pincode = request.POST['zip']
        updateuser.profile.phonenumber = request.POST['phone']
        updateuser.save()
        messages.success(request, 'User details updated successfully')
    except Exception as e:
        messages.error(request, 'Error: Detail changing failed. Reason:- '+ str(e))
    context = {'profiledata': profiledata}
    return redirect('/customeraccount')