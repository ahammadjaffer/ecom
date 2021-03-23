from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import connection
from portal.models import *

def viewallproducts(request):
    context = {}
    return render(request, 'portal/viewallproducts.html', context)

def viewproductdetail(request, productid):
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
        print(productdict)
    context = {'data':productdict}
    return render(request, 'portal/productdetail.html', context)

def basket(request):
    context = {}
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