from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.db import IntegrityError
from datetime import datetime
from ..models import *

# exception
import traceback
# transaction
from django.db import DatabaseError, transaction

@login_required(login_url='user_login')
def dashboard(request):
    context = {}
    companydetails = Companydetails.objects.all()
    return render(request, 'portal/admin/dashboard.html', context)

@login_required(login_url='user_login')
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

@login_required(login_url='user_login')
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

@login_required(login_url='user_login')
def adminlist(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'portal/admin/profilelist.html', context)

@login_required(login_url='user_login')
def productcategory(request):
    try:
        if request.method == 'POST':
            with transaction.atomic():
                categoryname = request.POST['categoryname']
                obj = Category(name=categoryname,status=1)
                obj.save()
                catid = obj.pk
                subcat = request.POST.getlist('subcategory')
                for value in subcat:
                    objsubcat = SubCategory(parentcategory=obj, name=value,status=1)
                    objsubcat.save()
                messages.success(request, 'Saved Successfully!')
    except Exception as e:
        messages.error(request, 'Error: Category not added. Reason:- '+ str(e))
        # print(traceback.format_exc())
    categories = Category.objects.filter(status=1)
    context = {'categories': categories}
    return render(request, 'portal/admin/productcategory.html', context)

@login_required(login_url='user_login')
def updatecategory(request):
    try:
        with transaction.atomic():
            category = Category.objects.get(id=request.POST['categoryid'])
            category.name=request.POST['editcategoryname']
            category.save()
            subcat = request.POST.getlist('subcategory')
            for value in subcat:
                if '_' not in value:
                    objsubcat = SubCategory(parentcategory=category, name=value,status=1)
                    objsubcat.save()
            messages.success(request, 'Category updated succesfully')
    except Exception as e:
        messages.error(request, 'Error: Category not updated. Reason:- '+ str(e))
    categories = Category.objects.filter(status=1)
    context = {'categories': categories}
    # return render(request, 'portal/admin/productcategory.html', context)
    return HttpResponseRedirect('/productcategory/')

@login_required(login_url='user_login')
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

@login_required(login_url='user_login')
def loadcategorymodal(request):
    if request.method == 'GET':
        data = []
        categoryid = request.GET['categoryid']
        details = SubCategory.objects.filter(parentcategory=categoryid, status=1)
        for detail in details:
            subcattemp = {}
            subcattemp['id'] = detail.id
            subcattemp['name'] = detail.name
            data.append(subcattemp)
        return JsonResponse({"instance": data}, status=200)

@login_required(login_url='user_login')
def deletesubcategory(request):
    if request.method == 'GET':
        try:
            subcategoryid = request.GET['subcategoryid']
            objsubcat = SubCategory.objects.get(id=subcategoryid)
            objsubcat.status=2
            objsubcat.save()
        except Exception as e:
            messages.success(request, 'Error: Subcategory delete failed. Reason:- '+ str(e))
        return JsonResponse({"subcategoryid": subcategoryid}, status=200)

@login_required(login_url='user_login')
def productlist(request):
    if request.method == 'POST':
        seperator = '$$'
        feature = ''
        if validateproduct(request):
            if "feature" in request.POST:
                feature = seperator.join(request.POST.getlist('feature'))
            product = Products.objects.create(name=request.POST['name'], 
            description=request.POST['description'], 
            features=feature, 
            categoryid=request.POST['productaddcategory'], 
            subcategoryid=request.POST['productaddsubcategory'], 
            count=request.POST['count'], 
            price=request.POST['price'], 
            sellerid=request.user.id, 
            status=1, 
            shipmentcharge=request.POST['shippingcharge'])
            for f in request.FILES.getlist('pro-image'):
                productimage = ProductImages.objects.create(productid=product, productImage=f)
            messages.success(request, 'Product added succesfully')
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
    return render(request, 'portal/admin/productlist.html', context)

@login_required(login_url='user_login')
def validateproduct(request):
    flag=False
    if request.POST['name']=='':
        messages.warning(request, 'Name cannot be empty')
        flag=True
    if request.POST['description']=='':
        messages.warning(request, 'Description cannot be empty')
        flag=True
    if request.POST['productaddcategory']=='':
        messages.warning(request, 'Category must be provided')
        flag=True
    if request.POST['productaddsubcategory']=='':
        messages.warning(request, 'Sub Category must be provided')
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

@login_required(login_url='user_login')
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

@login_required(login_url='user_login')
def updateproduct(request):
    if validateupdateproduct(request):
        seperator = '$$'
        feature = ''
        try:
            if "feature" in request.POST:
                feature = seperator.join(request.POST.getlist('feature'))
            product = Products.objects.get(id=request.POST['productid'])
            product.name=request.POST['editname']
            product.description=request.POST['editdescription']
            product.features=feature
            product.categoryid=request.POST['producteditcategory']
            product.subcategoryid=request.POST['producteditsubcategory']
            product.count=request.POST['editcount']
            product.price=request.POST['editprice']
            product.sellerid=request.user.id
            product.shipmentcharge=request.POST['editshippingcharge']
            product.save()
            messages.success(request, 'Prodect updated succesfully')
        except Exception as e:
            messages.success(request, 'Error: Product not updated. Reason:- '+ str(e))
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
    return render(request, 'portal/admin/productlist.html', context)

@login_required(login_url='user_login')
def validateupdateproduct(request):
    flag=False
    if request.POST['editname']=='':
        messages.warning(request, 'Name cannot be empty')
        flag=True
    if request.POST['editdescription']=='':
        messages.warning(request, 'Description cannot be empty')
        flag=True
    if request.POST['producteditcategory']=='':
        messages.warning(request, 'Category must be provided')
        flag=True
    if request.POST['producteditsubcategory']=='':
        messages.warning(request, 'Sub Category must be provided')
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

@login_required(login_url='user_login')
def loadproductmodal(request):
    if request.method == 'GET':
        data = []
        productid = request.GET['productid']
        details = Products.objects.filter(id=productid)
        for detail in details:
            producttemp = {}
            producttemp['id'] = detail.id
            producttemp['name'] = detail.name
            producttemp['description'] = detail.description
            producttemp['shippingcharge'] = detail.shipmentcharge
            producttemp['count'] = detail.count
            producttemp['price'] = detail.price
            producttemp['categoryid'] = detail.categoryid
            producttemp['subcategoryid'] = detail.subcategoryid
            producttemp['featurelist'] = detail.features.split('$$')
        data.append(producttemp)
        return JsonResponse({"instance": data}, status=200)

@login_required(login_url='user_login')
def loadproductaddmodal(request):
    if request.method == 'GET':
        data = []
        data = getcategory(request)
        return JsonResponse({"instance": data}, status=200)

# @login_required(login_url='user_login')
def loadmodalsubcategory(request):
    if request.method == 'GET':
        categoryid = request.GET['categoryid']
        data = []
        data = getsubcategory(categoryid)
        return JsonResponse({"instance":data}, status=200)

@login_required(login_url='user_login')
def getcategory(request):
    data = []
    categories = Category.objects.filter(status=1)
    for category in categories:
        categorytemp = {}
        categorytemp['id'] = category.id
        categorytemp['name'] = category.name
        data.append(categorytemp)
    return data

# @login_required(login_url='user_login')
def getsubcategory(categoryid):
    data = []
    subcategories = SubCategory.objects.filter(parentcategory=categoryid, status=1)
    for subcategory in subcategories:
        subcategorytemp = {}
        subcategorytemp['id'] = subcategory.id
        subcategorytemp['name'] = subcategory.name
        data.append(subcategorytemp)
    return data

@login_required(login_url='user_login')
def pendingorders(request):
    try:
        orders = Order.objects.filter(status=1)
        context = {'orders': orders}
        return render(request, 'portal/admin/pendingorders.html', context)
    except Exception as e:
        messages.success(request, 'Error: Could not load pending orders page. Reason:- '+ str(e))

@login_required(login_url='user_login')
def ordersindelivery(request):
    try:
        orders = Order.objects.filter(status=2)
        context = {'orders': orders}
        return render(request, 'portal/admin/ordersindelivery.html', context)
    except Exception as e:
        messages.success(request, 'Error: Could not load orders indelivery page. Reason:- '+ str(e))

@login_required(login_url='user_login')
def deliveredorders(request):
    try:
        orders = Order.objects.filter(status=3)
        context = {'orders': orders}
        return render(request, 'portal/admin/deliveredorders.html', context)
    except Exception as e:
        messages.success(request, 'Error: Could not load delivered orders page. Reason:- '+ str(e))

@login_required(login_url='user_login')
def cancelledorders(request):
    try:
        orders = Order.objects.filter(status=4)
        context = {'orders': orders}
        return render(request, 'portal/admin/cancelledorders.html', context)
    except Exception as e:
        messages.success(request, 'Error: Could not load cancelled orders page. Reason:- '+ str(e))

@login_required(login_url='user_login')
def pendingorderdetails(request):
    if request.method == 'GET':
        data = []
        ordertemp = {}
        orderdetailsjson = []
        orderid = request.GET['orderid']
        details = Order.objects.filter(id=orderid).select_related('clientid_id').values()
        for detail in details:
            orderdetails = OrderDetails.objects.filter(orderid_id=detail['id']).values()
            for orderdetail in orderdetails:
                productdetails = Products.objects.filter(id=orderdetail['productid_id']).values()[0]
                orderdetail['productname']=productdetails['name']
                orderdetail['shippingcharge']=productdetails['shipmentcharge']
                orderdetailsjson.append(orderdetail)
            clientdetail = User.objects.filter(id=detail['clientid_id'])[0]
            ordertemp['id'] = detail['id']
            ordertemp['paymentmode'] = detail['paymentmode']
            ordertemp['orderdate'] = detail['orderdate']
            ordertemp['grandtotal'] = detail['grandtotal']
            ordertemp['customername'] = clientdetail.first_name+' '+clientdetail.last_name
            ordertemp['email'] = clientdetail.email
            ordertemp['phonenumber'] = clientdetail.profile.phonenumber
            ordertemp['address'] = clientdetail.profile.address1
            ordertemp['pincode'] = clientdetail.profile.pincode
        data.append(ordertemp)
        return JsonResponse({"instance": data, "orderdetailsjson": orderdetailsjson}, status=200)

@login_required(login_url='user_login')
def acceptpendingorder(request):
    if request.method == 'GET':
        orderid = request.GET['orderid']
        try:
            product = Order.objects.get(id=orderid)
            product.status=2
            product.orderaccepteddate=datetime.now()
            product.save()
            messages.success(request, 'Order accepted succesfully')
        except Exception as e:
            messages.success(request, 'Error: Order accepting failed. Reason:- '+ str(e))
        return JsonResponse({"orderid": orderid}, status=200)

@login_required(login_url='user_login')
def orderindeliverydetails(request):
    if request.method == 'GET':
        data = []
        ordertemp = {}
        orderdetailsjson = []
        orderid = request.GET['orderid']
        details = Order.objects.filter(id=orderid).select_related('clientid_id').values()
        for detail in details:
            orderdetails = OrderDetails.objects.filter(orderid_id=detail['id']).values()
            for orderdetail in orderdetails:
                productdetails = Products.objects.filter(id=orderdetail['productid_id']).values()[0]
                orderdetail['productname']=productdetails['name']
                orderdetail['shippingcharge']=productdetails['shipmentcharge']
                orderdetailsjson.append(orderdetail)
            clientdetail = User.objects.filter(id=detail['clientid_id'])[0]
            ordertemp['id'] = detail['id']
            ordertemp['paymentmode'] = detail['paymentmode']
            ordertemp['orderdate'] = detail['orderdate']
            ordertemp['orderaccepteddate'] = detail['orderaccepteddate']
            ordertemp['grandtotal'] = detail['grandtotal']
            ordertemp['deliverystatus'] = detail['status']
            ordertemp['customername'] = clientdetail.first_name+' '+clientdetail.last_name
            ordertemp['email'] = clientdetail.email
            ordertemp['phonenumber'] = clientdetail.profile.phonenumber
            ordertemp['address'] = clientdetail.profile.address1
            ordertemp['pincode'] = clientdetail.profile.pincode
        data.append(ordertemp)
        return JsonResponse({"instance": data, "orderdetailsjson": orderdetailsjson}, status=200)

@login_required(login_url='user_login')
def billorderbyadmin(request):
    if request.method == 'GET':
        orderid = request.GET['orderid']
        isfulfilled = request.GET['isfulfilled']
        deliveredaddress = request.GET['deliveredaddress']
        if(isfulfilled):
            isfulfilled=1
        try:
            product = Order.objects.get(id=orderid)
            product.status=3
            product.isfulfilled=isfulfilled
            product.deliveredaddress=deliveredaddress
            product.billeddate=datetime.now()
            product.save()
            messages.success(request, 'Order billed succesfully')
        except Exception as e:
            messages.success(request, 'Error: Order billing failed. Reason:- '+ str(e))
        return JsonResponse({"orderid": orderid}, status=200)

@login_required(login_url='user_login')
def cancelorderbyadmin(request):
    if request.method == 'GET':
        orderid = request.GET['orderid']
        try:
            product = Order.objects.get(id=orderid)
            product.status=4
            product.isdeleted=1
            product.enddate=datetime.now()
            product.save()
            messages.success(request, 'Order cancelled succesfully')
        except Exception as e:
            messages.success(request, 'Error: Order cancelling failed. Reason:- '+ str(e))
        return JsonResponse({"orderid": orderid}, status=200)

@login_required(login_url='user_login')
def deliveredorderdetails(request):
    if request.method == 'GET':
        data = []
        ordertemp = {}
        orderdetailsjson = []
        orderid = request.GET['orderid']
        details = Order.objects.filter(id=orderid).select_related('clientid_id').values()
        for detail in details:
            orderdetails = OrderDetails.objects.filter(orderid_id=detail['id']).values()
            for orderdetail in orderdetails:
                productdetails = Products.objects.filter(id=orderdetail['productid_id']).values()[0]
                orderdetail['productname']=productdetails['name']
                orderdetail['shippingcharge']=productdetails['shipmentcharge']
                orderdetailsjson.append(orderdetail)
            clientdetail = User.objects.filter(id=detail['clientid_id'])[0]
            ordertemp['id'] = detail['id']
            ordertemp['paymentmode'] = detail['paymentmode']
            ordertemp['orderdate'] = detail['orderdate']
            ordertemp['orderaccepteddate'] = detail['orderaccepteddate']
            ordertemp['billeddate'] = detail['billeddate']
            ordertemp['grandtotal'] = detail['grandtotal']
            ordertemp['deliverystatus'] = detail['status']
            ordertemp['deliveredaddress'] = detail['deliveredaddress']
            ordertemp['customername'] = clientdetail.first_name+' '+clientdetail.last_name
            ordertemp['email'] = clientdetail.email
            ordertemp['phonenumber'] = clientdetail.profile.phonenumber
            ordertemp['address'] = clientdetail.profile.address1
            ordertemp['pincode'] = clientdetail.profile.pincode
        data.append(ordertemp)
        return JsonResponse({"instance": data, "orderdetailsjson": orderdetailsjson}, status=200)

@login_required(login_url='user_login')
def cancelledorderdetails(request):
    if request.method == 'GET':
        data = []
        ordertemp = {}
        orderdetailsjson = []
        orderid = request.GET['orderid']
        details = Order.objects.filter(id=orderid).select_related('clientid_id').values()
        for detail in details:
            orderdetails = OrderDetails.objects.filter(orderid_id=detail['id']).values()
            for orderdetail in orderdetails:
                productdetails = Products.objects.filter(id=orderdetail['productid_id']).values()[0]
                orderdetail['productname']=productdetails['name']
                orderdetail['shippingcharge']=productdetails['shipmentcharge']
                orderdetailsjson.append(orderdetail)
            clientdetail = User.objects.filter(id=detail['clientid_id'])[0]
            ordertemp['id'] = detail['id']
            ordertemp['paymentmode'] = detail['paymentmode']
            ordertemp['orderdate'] = detail['orderdate']
            ordertemp['orderaccepteddate'] = detail['orderaccepteddate']
            ordertemp['enddate'] = detail['enddate']
            ordertemp['grandtotal'] = detail['grandtotal']
            ordertemp['deliverystatus'] = detail['status']
            ordertemp['customername'] = clientdetail.first_name+' '+clientdetail.last_name
            ordertemp['email'] = clientdetail.email
            ordertemp['phonenumber'] = clientdetail.profile.phonenumber
            ordertemp['address'] = clientdetail.profile.address1
            ordertemp['pincode'] = clientdetail.profile.pincode
        data.append(ordertemp)
        return JsonResponse({"instance": data, "orderdetailsjson": orderdetailsjson}, status=200)

@login_required(login_url='user_login')
def banners(request):
    if request.method == 'POST':
        bannertag = request.POST['bannertag']
        try:
            if len(request.FILES) != 0:
                _, file = request.FILES.popitem()
                file = file[0]
            obj, created = Banners.objects.update_or_create(bannertag=bannertag, defaults={'bannertag': bannertag, 'bannerimage': file} )
            messages.success(request, 'Banner updated successfully')
        except Exception as e:
            messages.error(request, 'Error: Banner image update failed. Reason:- '+ str(e))
    bannerdetails = getbanners()
    context = {'bannerdetails':bannerdetails}
    return render(request, 'portal/admin/banners.html', context)

def getbanners():
    try:
        bannerdict = {}
        bannerobj = Banners.objects.all()
        for banner in bannerobj:
            bannerdict[banner.bannertag] = banner.imageURL
        return bannerdict
    except Exception as e:
        messages.error(request, 'Error: Banner image load failed. Reason:- '+ str(e))

@login_required(login_url='user_login')
def companydetails(request):
    if request.method == 'POST':
        try:
            if len(request.FILES) != 0:
                _, file = request.FILES.popitem()
                file = file[0]
            obj, created = Companydetails.objects.update_or_create(companytag='c1', 
            defaults={'companytag': 'c1',
             'name': request.POST['companyname'],
             'address': request.POST['address'],
             'email': request.POST['email'],
             'phonenumber': request.POST['phonenumber'],
             'termsandconditions': request.POST['termsandconditions'],
             'companylogo': file,
             'facebook': request.POST['facebook'],
             'instagram': request.POST['instagram'],
             'youtube': request.POST['youtube']
             } )
            messages.success(request, 'Company details updated successfully')
        except Exception as e:
            messages.error(request, 'Error: Company details update failed. Reason:- '+ str(e))
    context = {}
    data = []
    try:
        companydetails = Companydetails.objects.all().values()
        for row in companydetails:
            data = row
        context = {'data':data}
    except Exception as e:
        messages.error(request, 'Error: Banner image load failed. Reason:- '+ str(e))
    return render(request, 'portal/admin/companydetails.html', context)