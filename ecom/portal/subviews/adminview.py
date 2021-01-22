from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError
from datetime import datetime
from ..models import *

def admin_home(request):
    context = {}
    return render(request, 'portal/adminhome.html', context)

def admin_profile(request):
    if request.method == 'POST':
        portaluserid = request.user.id
        updateuser = User.objects.get(username=request.user)
        updateuser.first_name = request.POST['firstname']
        updateuser.last_name = request.POST['lastname']
        updateuser.email = request.POST['email']
        updateuser.profile.address1 = request.POST['address1']
        updateuser.profile.address2 = request.POST['address2']
        updateuser.profile.phonenumber = request.POST['phone']
        updateuser.profile.pincode = request.POST['pincode']
        # updateuser = User(first_name=request.POST.get("firstname"), last_name=request.POST.get("lastname"), email=request.POST.get("email"))
        updateuser.save()
        messages.success(request, 'Saved Successfully')
        return redirect('/adminprofile/')
    profile = Profile.objects.filter(user_id=request.user.id)
    for p in profile:
        profiledata = p
    context = {'profiledata': profiledata}
    return render(request, 'portal/profile.html', context)

def changepassword(request):
    saveuser = User.objects.get(id=request.user.id)
    if saveuser.check_password(request.POST.get('password_old')):
        saveuser.set_password(request.POST['password_1'])
        saveuser.save()
    else:
        messages.success(request, 'Old password is incorrect')
    profile = Profile.objects.filter(user_id=request.user.id)
    for p in profile:
        profiledata = p
    context = {'profiledata': profiledata}
    return render(request, 'portal/profile.html', context)

def adminlist(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'portal/profilelist.html', context)

def productlist(request):
    if request.method == 'POST':
        if validateproduct(request):
            product = Products.objects.create(name=request.POST['name'], 
            description=request.POST['description'], 
            categoryid=request.POST['category'], 
            count=request.POST['count'], 
            price=request.POST['price'], 
            sellerid=request.user.id, 
            status=1, 
            shipmentcharge=request.POST['shippingcharge'])
            for f in request.FILES.getlist('pro-image'):
                productimage = ProductImages.objects.create(productid=product, productImage=f)
            messages.success(request, 'Prodect added succesfully')
    products = Products.objects.filter(status=1)
    data = []
    for product in products:
        producttemp = {}
        category = Category.objects.get(id=product.categoryid)
        producttemp['id'] = product.id
        producttemp['name'] = product.name
        producttemp['count'] = product.count
        producttemp['price'] = product.price
        producttemp['status'] = "Active" if product.status==1 else "Inactive"
        producttemp['categoryname'] = category.name
        data.append(producttemp)
    context = {'data': data}
    return render(request, 'portal/productlist.html', context)

def validateproduct(request):
    flag=False
    if request.POST['name']=='':
        messages.warning(request, 'Name cannot be empty')
        flag=True
    if request.POST['description']=='':
        messages.warning(request, 'Description cannot be empty')
        flag=True
    if request.POST['category']=='':
        messages.warning(request, 'Category must be provided')
        flag=True
    if request.POST['count']=='':
        messages.warning(request, 'Enter count of product')
        flag=True
    if request.POST['price']=='':
        messages.warning(request, 'Price cannot be empty')
        flag=True
    if request.POST['shippingcharge']=='':
        messages.warning(request, 'Shipping charge cannot be empty. If no charge applicable enter 0.')
        flag=True
    if flag==True:
        return False
    else:
        return True
            
def productcategory(request):
    if request.method == 'POST':
        categoryname = request.POST['categoryname']
        obj = Category(name=categoryname,status=1)
        obj.save()
    categories = Category.objects.filter(status=1)
    context = {'categories': categories}
    return render(request, 'portal/productcategory.html', context)

def loadproductmodal(request):
    if request.method == 'GET':
        data = []
        producttemp = {}
        productid = request.GET['productid']
        details = Products.objects.filter(id=productid)
        for detail in details:
            producttemp['id'] = detail.id
            producttemp['name'] = detail.name
            producttemp['description'] = detail.description
            producttemp['shippingcharge'] = detail.shipmentcharge
            producttemp['count'] = detail.count
            producttemp['price'] = detail.price
            producttemp['categoryid'] = detail.categoryid
        data.append(producttemp)
        return JsonResponse({"instance": data}, status=200)

def updateproduct(request):
    if validateupdateproduct(request):
        try:
            product = Products.objects.get(id=request.POST['productid'])
            product.name=request.POST['editname']
            product.description=request.POST['editdescription']
            product.categoryid=request.POST['editcategory']
            product.count=request.POST['editcount']
            product.price=request.POST['editprice']
            product.sellerid=request.user.id
            product.shipmentcharge=request.POST['editshippingcharge']
            product.save()
            messages.success(request, 'Prodect updated succesfully')
        except Exception as e:
            messages.success(request, 'Error: Product not updated. Reason:- '+ str(e))
    products = Products.objects.all()
    data = []
    producttemp = {}
    for product in products:
        category = Category.objects.get(id=product.categoryid)
        producttemp['id'] = product.id
        producttemp['name'] = product.name
        producttemp['count'] = product.count
        producttemp['price'] = product.price
        producttemp['status'] = "Active" if product.status==1 else "Inactive"
        producttemp['categoryname'] = category.name
    data.append(producttemp)
    context = {'data': data}
    return render(request, 'portal/productlist.html', context)

def validateupdateproduct(request):
    flag=False
    if request.POST['editname']=='':
        messages.warning(request, 'Name cannot be empty')
        flag=True
    if request.POST['editdescription']=='':
        messages.warning(request, 'Description cannot be empty')
        flag=True
    if request.POST['editcategory']=='':
        messages.warning(request, 'Category must be provided')
        flag=True
    if request.POST['editcount']=='':
        messages.warning(request, 'Enter count of product')
        flag=True
    if request.POST['editprice']=='':
        messages.warning(request, 'Price cannot be empty')
        flag=True
    if request.POST['editshippingcharge']=='':
        messages.warning(request, 'Shipping charge cannot be empty. If no charge applicable enter 0.')
        flag=True
    if flag==True:
        return False
    else:
        return True

def deleteproduct(request):
    if request.method == 'GET':
        productid = request.GET['productid']
        try:
            product = Products.objects.get(id=productid)
            product.enddate=datetime.now()
            product.status=0
            product.save()
            messages.success(request, 'Product deleted succesfully')
        except Exception as e:
            messages.success(request, 'Error: Product not deleted. Reason:- '+ str(e))
        return JsonResponse({"productid": productid}, status=200)

def updatecategory(request):
    try:
        category = Category.objects.get(id=request.POST['categoryid'])
        category.name=request.POST['editcategoryname']
        category.save()
        messages.success(request, 'Category updated succesfully')
    except Exception as e:
        messages.success(request, 'Error: Category not updated. Reason:- '+ str(e))
    categories = Category.objects.filter(status=1)
    context = {'categories': categories}
    return render(request, 'portal/productcategory.html', context)

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
            messages.success(request, 'Error: Category not deleted. Reason:- '+ str(e))
        return JsonResponse({"categoryid": categoryid}, status=200)

def manageorders(request):
    try:
        orders = Order.objects.filter(status=1)
        context = {'orders': orders}
        return render(request, 'portal/manageorders.html', context)
    except Exception as e:
        messages.success(request, 'Error: Could not load manage order page. Reason:- '+ str(e))

def pendingorders(request):
    try:
        context = {}
        return render(request, 'portal/pendingorders.html', context)
    except Exception as e:
        messages.success(request, 'Error: Could not load pending orders page. Reason:- '+ str(e))

def ordersindelivery(request):
    try:
        context = {}
        return render(request, 'portal/ordersindelivery.html', context)
    except Exception as e:
        messages.success(request, 'Error: Could not load orders indelivery page. Reason:- '+ str(e))

def deliveredorders(request):
    try:
        context = {}
        return render(request, 'portal/deliveredorders.html', context)
    except Exception as e:
        messages.success(request, 'Error: Could not load delivered orders page. Reason:- '+ str(e))

def cancelledorders(request):
    try:
        context = {}
        return render(request, 'portal/cancelledorders.html', context)
    except Exception as e:
        messages.success(request, 'Error: Could not load cancelled orders page. Reason:- '+ str(e))