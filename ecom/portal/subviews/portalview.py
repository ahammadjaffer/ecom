from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import connection
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import DatabaseError, transaction
from datetime import datetime
from portal.subviews import constants as cs
from portal.subviews import emails as em
from portal.models import *

def viewallproducts(request, categoryid, subcategoryid):
    detail = {}
    productlist = []
    if (subcategoryid==0):
        objproducts = Products.objects.filter(categoryid=categoryid, status=1).order_by('id')
    else:
        objproducts = Products.objects.filter(subcategoryid=subcategoryid, status=1).order_by('id')
    paginator = Paginator(objproducts, 12)
    page = request.GET.get('page', 1)
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        post_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        post_list = paginator.page(paginator.num_pages)
    for product in post_list:
        tempproduct = {}
        productimage = getproductimages(request, product.id)
        tempproduct['id'] = product.id
        tempproduct['name'] = product.name
        tempproduct['price'] = product.price
        tempproduct['image'] = productimage[1]
        productlist.append(tempproduct)
    detail['categoryid'] = categoryid
    detail['subcategoryid'] = subcategoryid
    detail['productlist'] = productlist
    detail['numberofproducts'] = len(post_list)
    detail['issearch'] = False
    context = {"data":post_list, "paginator":paginator, "detail":detail}
    return render(request, 'portal/viewallproducts.html', context)

def searchproducts(request):
    detail = {}
    productlist = []
    searchvalue = request.POST['searchvalue']
    objproducts = Products.objects.filter(name__contains=searchvalue).order_by('id')
    paginator = Paginator(objproducts, 12)
    page = request.GET.get('page', 1)
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        post_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        post_list = paginator.page(paginator.num_pages)
    for product in post_list:
        tempproduct = {}
        productimage = getproductimages(request, product.id)
        tempproduct['id'] = product.id
        tempproduct['name'] = product.name
        tempproduct['price'] = product.price
        tempproduct['image'] = productimage[1]
        productlist.append(tempproduct)
    detail['categoryid'] = product.categoryid
    detail['subcategoryid'] = product.subcategoryid
    detail['productlist'] = productlist
    detail['numberofproducts'] = len(post_list)
    detail['issearch'] = True
    context = {"data":post_list, "paginator":paginator, "detail":detail}
    return render(request, 'portal/viewallproducts.html', context)

def viewproductdetail(request, productid):
    productdict = {}
    productlist = []
    objproducts = Products.objects.filter(id=productid)
    for product in objproducts:
        productdict = {}
        productdict['id'] = product.id
        productdict['name'] = product.name
        productdict['description'] = product.description
        productdict['features'] = product.features.split('$$')
        productdict['deliverydetails'] = product.deliverydetails
        productdict['categoryid'] = product.categoryid
        productdict['subcategoryid'] = product.subcategoryid
        productdict['count'] = product.count
        productdict['price'] = product.price
        productdict['shipmentcharge'] = product.shipmentcharge
        objproductimages = ProductImages.objects.filter(productid=productid).values()
        productdict['productimages']=[]
        for image in objproductimages:
            tempimage = {}
            tempimage['image'] = image['productImage']
            productdict['productimages'].append(tempimage)
        productlist.append(productdict)
    context = {'data':productdict}
    return render(request, 'portal/productdetail.html', context)

@login_required(login_url='user_login')
def basket(request):
    detail = {}
    context = {}
    cartlist = []
    shipmentcharge = 0
    orderdetailids = []
    seperator = ','
    cartitemscount = 0
    if request.method == 'POST':
        updatecart(request)
    try:
        user = request.user
        order = Order.objects.filter(clientid=user, enddate__isnull=True, status=0)
        if (len(order)>0):
            detail['orderid'] = order[0].id
            detail['grandtotal'] = order[0].grandtotal
            orderdetails = OrderDetails.objects.filter(orderid=order[0], status=0)
            for orderdetail in orderdetails:
                carttemp = {}
                objproduct = Products.objects.filter(id=orderdetail.productid.id)[0]
                orderdetailids.append(str(orderdetail.id))
                carttemp['orderdetailid'] = orderdetail.id
                carttemp['producttotal'] = orderdetail.producttotal
                carttemp['productquantity'] = orderdetail.quantity
                carttemp['productid'] = objproduct.id
                carttemp['name'] = objproduct.name
                carttemp['price'] = objproduct.price
                carttemp['shipmentcharge'] = objproduct.shipmentcharge
                shipmentcharge = int(shipmentcharge)+int(objproduct.shipmentcharge)
                carttemp['count'] = objproduct.count
                productimage = getproductimages(request, objproduct.id)
                carttemp['productimage'] = productimage[1]
                cartlist.append(carttemp) 
                cartitemscount += 1
            orderdetailidsstring = seperator.join(orderdetailids)
            detail['orderdetailids'] = orderdetailidsstring
            detail['orderdetail'] = cartlist
            detail['shipmentcharge'] = shipmentcharge
            detail['cartitemscount'] = cartitemscount
    except Exception as e:
        messages.error(request, 'Error: Reason:- '+ str(e))
    context = {'detail':detail}
    return render(request, 'portal/basket.html', context)

def getproductsforhomepage(request):
    categoryids = [11,12,13]
    productbycat = {}
    for id in categoryids:
        productlist = []
        products = getproducts(request, id)
        for product in products:
            tempproduct = {}
            tempproduct['id'] = product[0]
            tempproduct['name'] = product[1]
            tempproduct['price'] = product[2]
            productimages = getproductimages(request, tempproduct['id'])
            tempproduct['image'] = productimages[1]
            productlist.append(tempproduct)
        productbycat[id] = productlist
    return productbycat

def getproducts(request, id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("select id as id, name, price from portal_products where categoryid = %s and count >0 and status=1 order by id limit 12", [id])
            row = cursor.fetchall()
            return row
    except Exception as e:
        messages.success(request, 'Error: Could not load products. category id - '+ str(id) +' Reason:- '+ str(e))

def getproductimages(request, id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("select * from portal_productimages where productid_id = %s", [id])
            row = cursor.fetchone()
            return row
    except Exception as e:
        messages.success(request, 'Error: Could not load product images. category id - '+ str(id) +' Reason:- '+ str(e))

def addtocartdetail(request, productid):
    try:
        if request.user.is_authenticated:
            addtocart(request, productid)
        else:
            messages.warning(request, 'Please login to use cart')
        return redirect('/viewproductdetail/'+str(productid)+'/')
    except Exception as e:
        messages.warning(request, 'Error: Reason:- '+ str(e))
    return redirect('/viewproductdetail/'+str(productid)+'/')

def addtocartlist(request, categoryid, subcategoryid, productid, issearch):
    try:
        if request.user.is_authenticated:
            addtocart(request, productid)
        else:
            messages.warning(request, 'Please login to use cart')
        return redirect('/viewallproducts/'+str(categoryid)+'/'+str(subcategoryid))
    except Exception as e:
        messages.warning(request, 'Error: Reason:- '+ str(e))
    return redirect('/viewallproducts/'+str(categoryid)+'/'+str(subcategoryid))

def addtocarthome(request, productid):
    try:
        if request.user.is_authenticated:
            addtocart(request, productid)
        else:
            messages.warning(request, 'Please login to use cart')
        return redirect('/')
    except Exception as e:
        messages.warning(request, 'Error: Reason:- '+ str(e))
    return redirect('/')

def addtocart(request, productid):
    try:
        with transaction.atomic():
            user = request.user
            objproduct = Products.objects.filter(id=productid)[0]
            userid = user.id
            quantity = 0
            producttotal = 0
            grandtotal = 0
            productcount = objproduct.count
            order = Order.objects.filter(clientid=user, enddate__isnull=True, status=0)
            if (not len(order)>0):
                # Add order
                quantity = 1
                producttotal = objproduct.price
                grandtotal = int(objproduct.price)+int(objproduct.shipmentcharge)
                objorder = Order(clientid=user, grandtotal=grandtotal, status=0)
                objorder.save()
                orderid = objorder.pk
                # Add order details
                objorderdetail = OrderDetails(orderid=objorder, productid=objproduct, quantity=quantity, producttotal=producttotal, status=0)
                objorderdetail.save()
                messages.success(request, 'Added to cart')
            else:
                order = order[0]
                orderid = order.id
                gtotalincart = order.grandtotal
                quantity = 1
                producttotal = objproduct.price
                gtotal = int(gtotalincart)+int(objproduct.price)
                # update order
                objorder = Order.objects.get(id=orderid)
                objorder.grandtotal = gtotal
                objorder.updateddate = datetime.now()
                objorder.save()
                # check for product in order detail
                orderdetail = OrderDetails.objects.filter(orderid=objorder, productid=objproduct, status=0)
                if (not len(orderdetail)>0):
                    # Add shipment to grand total
                    objorder = Order.objects.get(id=orderid)
                    objorder.grandtotal = gtotal+int(objproduct.shipmentcharge)
                    objorder.save()
                    # Add order details
                    objorderdetail = OrderDetails(orderid=objorder, productid=objproduct, quantity=quantity, producttotal=producttotal, status=0)
                    objorderdetail.save()
                else:
                    orderdetail = orderdetail[0]
                    # Update order details
                    orderdetailid = orderdetail.id
                    orderdetailquantity = orderdetail.quantity
                    orderdetailptotal = orderdetail.producttotal
                    producttotal = int(producttotal)+int(orderdetailptotal)
                    quantity = int(orderdetailquantity)+1
                    objorderdetail = OrderDetails.objects.get(id=orderdetailid)
                    objorderdetail.quantity = quantity
                    objorderdetail.producttotal = producttotal
                    objorderdetail.updateddate = datetime.now()
                    objorderdetail.save()
                messages.success(request, 'Cart updated')
    except Exception as e:
        messages.warning(request, 'Error: Reason:- '+ str(e))

def deletecartitem(request):
    try:
        with transaction.atomic():
            orderdetailid = request.GET['orderdetailid']
            objorderdetail = OrderDetails.objects.filter(id=orderdetailid).values()[0]
            orderid = objorderdetail['orderid_id']
            producttotal = objorderdetail['producttotal']
            updateddate = datetime.now()
            objorder = Order.objects.get(id=orderid)
            objproduct = Products.objects.filter(id=objorderdetail['productid_id'])[0]
            grandtotal = objorder.grandtotal
            grandtotal = int(grandtotal)-(int(producttotal)+int(objproduct.shipmentcharge))
            objorder.grandtotal = grandtotal
            objorder.updateddate = updateddate
            objorder.save()
            objorderdetailnew = OrderDetails.objects.get(pk=orderdetailid)
            objorderdetailnew.delete()
        messages.success(request, 'Cart item removed')
    except Exception as e:
        messages.error(request, 'Error:Removing item from cart failed. Reason:- '+ str(e))
    return JsonResponse({"orderdetailid": orderdetailid}, status=200)

def updatecart(request):
    try:
        with transaction.atomic():
            odids = request.POST['orderdetailids']
            cartlist = request.POST.getlist('cartlist')
            orderid = request.POST['orderid']
            grandtotal = request.POST['grandtotal']
            odidslist = odids.split(',')
            for odid in odidslist:
                orderdetailid = request.POST['cartlist['+odid+'][orderdetailid]']
                productquantity = request.POST['cartlist['+odid+'][productquantity]']
                oldproductquantity = request.POST['cartlist['+odid+'][oldproductquantity]']
                producttotal = request.POST['cartlist['+odid+'][producttotal]']
                objorderdetails = OrderDetails.objects.get(id=orderdetailid)
                objorderdetails.quantity = productquantity
                objorderdetails.producttotal = producttotal
                objorderdetails.save()
            objorder = Order.objects.get(id=orderid)
            objorder.grandtotal = grandtotal
            objorder.save()
            messages.success(request, 'Cart updated')
    except Exception as e:
        messages.error(request, 'Error: Cart update failed. Reason:- '+ str(e))

@login_required(login_url='user_login')
def checkout(request):
    data = {}
    userdetails = {}
    cartlist = []
    shipmentcharge = 0
    subtotal = 0
    user = request.user
    order = Order.objects.filter(clientid=user, enddate__isnull=True, status=0)
    data['orderid'] = order[0].id
    data['grandtotal'] = order[0].grandtotal
    orderdetails = OrderDetails.objects.filter(orderid=order[0], status=0)
    for orderdetail in orderdetails:
        objproduct = Products.objects.filter(id=orderdetail.productid.id)[0]
        subtotal  = int(subtotal)+int(orderdetail.producttotal)
        shipmentcharge = int(shipmentcharge)+int(objproduct.shipmentcharge)
    data['shipmentcharge'] = shipmentcharge
    data['subtotal'] = subtotal
    # User details
    userdetails['firstname'] = user.first_name
    userdetails['lastname'] = user.last_name
    userdetails['email'] = user.email
    clientdetail = User.objects.filter(id=user.id)[0]
    userdetails['phone'] = clientdetail.profile.phonenumber
    userdetails['address'] = '' if(clientdetail.profile.housename =='' or clientdetail.profile.housename ==None) else clientdetail.profile.housename
    userdetails['street'] = '' if(clientdetail.profile.street =='' or clientdetail.profile.street ==None) else clientdetail.profile.street
    userdetails['landmark'] = '' if(clientdetail.profile.landmark =='' or clientdetail.profile.landmark ==None) else clientdetail.profile.landmark
    userdetails['zipcode'] = clientdetail.profile.pincode
    data['userdetails'] = userdetails

    if (len(order)>0):
        orderdetails = OrderDetails.objects.filter(orderid=order[0], status=0)
        for orderdetail in orderdetails:
            carttemp = {}
            objproduct = Products.objects.filter(id=orderdetail.productid.id)[0]
            carttemp['producttotal'] = orderdetail.producttotal
            carttemp['productquantity'] = orderdetail.quantity
            carttemp['name'] = objproduct.name
            carttemp['price'] = objproduct.price
            carttemp['shipmentcharge'] = objproduct.shipmentcharge
            shipmentcharge = int(shipmentcharge)+int(objproduct.shipmentcharge)
            productimage = getproductimages(request, objproduct.id)
            carttemp['productimage'] = productimage[1]
            cartlist.append(carttemp) 
        data['orderdetail'] = cartlist

    context={'data':data}
    return render(request, 'portal/checkout.html', context)

@login_required(login_url='user_login')
def ordersubmit(request):
    try:
        updateddate = datetime.now()
        userid = request.user.id
        # transaction start
        with transaction.atomic():
            # update user details
            updateuser = User.objects.get(username=request.user)
            updateuser.profile.housename = request.POST['house']
            updateuser.profile.street = request.POST['street']
            updateuser.profile.landmark = request.POST['landmark']
            updateuser.profile.state = request.POST['state']
            updateuser.profile.country = request.POST['country']
            updateuser.profile.pincode = request.POST['zip']
            updateuser.save()
            # update order
            objorder = Order.objects.get(id=request.POST['orderid'])
            objorder.status = cs.order_ordered
            objorder.updateddate = updateddate
            objorder.paymentmode = request.POST['payment']
            objorder.paymentstatus = cs.payment_notdone
            objorder.save()
            # update product count
            orderdetails = OrderDetails.objects.filter(orderid=request.POST['orderid'])
            for orderdetail in orderdetails:
                quantity = orderdetail.quantity
                product = Products.objects.get(id=orderdetail.productid.id)
                if product.count < 1:
                    raise ValueError(product.name+' is out of stock')
                else:
                    productcount = product.count
                    productcount = int(productcount)-int(quantity)
                    if productcount < 1:
                        raise ValueError(product.name+' is not available in requested quantity')
                    else:
                        product.count = productcount
                        product.save()
            # payment gateway call
            # email notification call
            em.ordermade(request, userid)

        # transation commit
        messages.success(request, 'Order placed')
    except Exception as e:
        messages.error(request, 'Order failed. Reason:- '+ str(e))
    return redirect('/')

@login_required(login_url='user_login')
def orderhistory(request):
    try:
        user = request.user
        data = []
        orders = Order.objects.filter(clientid=user, status__in = (1, 2, 3))
        if (len(orders)>0):
            for order in orders:
                orderdetailids = []
                cartlist = []
                seperator = ','
                shipmentcharge = 0
                detail = {}
                detail['orderid'] = order.id
                detail['grandtotal'] = order.grandtotal
                if int(order.status) in (1, 2):
                    detail['cancancel'] = True
                else:
                    detail['cancancel'] = False
                orderdetails = OrderDetails.objects.filter(orderid=order.id, status=0)
                for orderdetail in orderdetails:
                    carttemp = {}
                    objproduct = Products.objects.filter(id=orderdetail.productid.id)[0]
                    orderdetailids.append(str(orderdetail.id))
                    carttemp['orderdetailid'] = orderdetail.id
                    carttemp['producttotal'] = orderdetail.producttotal
                    carttemp['productquantity'] = orderdetail.quantity
                    carttemp['productid'] = objproduct.id
                    carttemp['name'] = objproduct.name
                    carttemp['price'] = objproduct.price
                    carttemp['shipmentcharge'] = objproduct.shipmentcharge
                    shipmentcharge = int(shipmentcharge)+int(objproduct.shipmentcharge)
                    carttemp['count'] = objproduct.count
                    productimage = getproductimages(request, objproduct.id)
                    carttemp['productimage'] = productimage[1]
                    cartlist.append(carttemp) 
                orderdetailidsstring = seperator.join(orderdetailids)
                detail['orderdetailids'] = orderdetailidsstring
                detail['orderdetail'] = cartlist
                detail['shipmentcharge'] = shipmentcharge
                data.append(detail)
    except Exception as e:
        messages.error(request, 'Error: Reason:- '+ str(e))
    context = {'datalist':data}
    return render(request, 'portal/orderhistory.html', context)

@login_required(login_url='user_login')
def cancelorder(request, orderid):
    try:
        userid = request.user.id
        updateddate = datetime.now()
        with transaction.atomic():
            # update order
            objorder = Order.objects.get(id=orderid)
            objorder.status = cs.order_cancelled
            objorder.updateddate = updateddate
            objorder.enddate = updateddate
            objorder.save()
            orderdetails = OrderDetails.objects.filter(orderid=orderid)
            for orderdetail in orderdetails:
                # update each order detail
                orderdetailsdr = OrderDetails.objects.get(id=orderdetail.id)
                orderdetailsdr.updateddate = updateddate
                orderdetailsdr.status = cs.Orderdetail_inactive
                orderdetailsdr.save()
                # update product count
                quantity = orderdetail.quantity
                product = Products.objects.get(id=orderdetail.productid.id)
                productcount = product.count
                productcount = int(productcount)+int(quantity)
                product.count = productcount
                product.save()
            # payment gateway refund
            em.ordercancelled(request, userid)
                
    except Exception as e:
        messages.error(request, 'Error: Reason:- '+ str(e))
    return redirect('/orderhistory')

@login_required(login_url='user_login')
def buynow(request, productid):
    try:
        print(productid)
        if request.user.is_authenticated:
            addtocart(request, productid)
        else:
            messages.warning(request, 'Please login to use cart')
    except Exception as e:
        messages.error(request, 'Error: Reason:- '+ str(e))
    return redirect('/checkout/')