from django.urls import path

from . import views
from .subviews import adminview, portalview, adminpanelview
from .subviews import useraccount
from .subviews import contactform

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('adminhome/', adminview.admin_home, name='admin_home'),
    # path('adminprofile/', adminview.admin_profile, name='admin_profile'),
    # path('changepassword/', adminview.changepassword, name='changepassword'),
    # path('adminlist/', adminview.adminlist, name='adminlist'),
    # path('productlist/', adminview.productlist, name='productlist'),
    # path('productcategory/', adminview.productcategory, name='productcategory'),
    # path('loadproductmodal/', adminview.loadproductmodal, name='loadproductmodal'),
    # path('updateproduct/', adminview.updateproduct, name='updateproduct'),
    # path('deleteproduct/', adminview.deleteproduct, name='deleteproduct'),
    # path('updatecategory/', adminview.updatecategory, name='updatecategory'),
    # path('deletecategory/', adminview.deletecategory, name='deletecategory'),
    path('manageorders/', adminview.manageorders, name='manageorders'),
    # path('pendingorders/', adminview.pendingorders, name='pendingorders'),
    # path('ordersindelivery/', adminview.ordersindelivery, name='ordersindelivery'),
    # path('deliveredorders/', adminview.deliveredorders, name='deliveredorders'),
    # path('cancelledorders/', adminview.cancelledorders, name='cancelledorders'),
    # path('pendingorderdetails/', adminview.pendingorderdetails, name='pendingorderdetails'),
    # path('acceptpendingorder/', adminview.acceptpendingorder, name='acceptpendingorder'),
    # path('orderindeliverydetails/', adminview.orderindeliverydetails, name='orderindeliverydetails'),
    # path('billorderbyadmin/', adminview.billorderbyadmin, name='billorderbyadmin'),
    # path('cancelorderbyadmin/', adminview.cancelorderbyadmin, name='cancelorderbyadmin'),
    # path('deliveredorderdetails/', adminview.deliveredorderdetails, name='deliveredorderdetails'),
    # path('cancelledorderdetails/', adminview.cancelledorderdetails, name='cancelledorderdetails'),
    path('viewallproducts/<int:categoryid>/<int:subcategoryid>', portalview.viewallproducts, name='viewallproducts'),
    path('viewproductdetail/<int:productid>/', portalview.viewproductdetail, name='viewproductdetail'),
    path('basket/', portalview.basket, name='basket'),
    path('addtocartdetail/<int:productid>/', portalview.addtocartdetail, name='addtocartdetail'),
    path('addtocarthome/<int:productid>/', portalview.addtocarthome, name='addtocarthome'),
    path('addtocartlist/<int:categoryid>/<int:subcategoryid>/<int:productid>/', portalview.addtocartlist, name='addtocartlist'),
    path('deletecartitem/', portalview.deletecartitem, name='deletecartitem'),
    path('checkout/', portalview.checkout, name='checkout'),
    path('ordersubmit/', portalview.ordersubmit, name='ordersubmit'),
    path('customeraccount/', useraccount.customeraccount, name='customeraccount'),
    path('changecustomerpassword/', useraccount.changecustomerpassword, name='changecustomerpassword'),
    path('changecustomerdetails/', useraccount.changecustomerdetails, name='changecustomerdetails'),
    path('contactindex/', contactform.contactindex, name='contactindex'),
    path('sendemail/', contactform.sendemail, name='sendemail'),
    path('orderhistory/', portalview.orderhistory, name='orderhistory'),
    path('cancelorder/<int:orderid>/', portalview.cancelorder, name='cancelorder'),
    path('buynow/<int:productid>/', portalview.buynow, name='buynow'),
    path('searchproducts/', portalview.searchproducts, name='searchproducts'),

    # new admin pages
    path('dashboard/', adminpanelview.dashboard, name='dashboard'),
    path('adminprofile/', adminpanelview.admin_profile, name='admin_profile'),
    path('changepassword/', adminpanelview.changepassword, name='changepassword'),
    path('adminlist/', adminpanelview.adminlist, name='adminlist'),
    path('productcategory/', adminpanelview.productcategory, name='productcategory'),
    path('updatecategory/', adminpanelview.updatecategory, name='updatecategory'),
    path('deletecategory/', adminpanelview.deletecategory, name='deletecategory'),
    path('loadcategorymodal/', adminpanelview.loadcategorymodal, name='loadcategorymodal'),
    path('deletesubcategory/', adminpanelview.deletesubcategory, name='deletesubcategory'),
    path('productlist/', adminpanelview.productlist, name='productlist'),
    path('loadproductaddmodal/', adminpanelview.loadproductaddmodal, name='loadproductaddmodal'),
    path('loadmodalsubcategory/', adminpanelview.loadmodalsubcategory, name='loadmodalsubcategory'),
    path('loadproductmodal/', adminpanelview.loadproductmodal, name='loadproductmodal'),
    path('updateproduct/', adminpanelview.updateproduct, name='updateproduct'),
    path('deleteproduct/', adminpanelview.deleteproduct, name='deleteproduct'),
    path('pendingorders/', adminpanelview.pendingorders, name='pendingorders'),
    path('ordersindelivery/', adminpanelview.ordersindelivery, name='ordersindelivery'),
    path('deliveredorders/', adminpanelview.deliveredorders, name='deliveredorders'),
    path('cancelledorders/', adminpanelview.cancelledorders, name='cancelledorders'),
    path('pendingorderdetails/', adminpanelview.pendingorderdetails, name='pendingorderdetails'),
    path('acceptpendingorder/', adminpanelview.acceptpendingorder, name='acceptpendingorder'),
    path('orderindeliverydetails/', adminpanelview.orderindeliverydetails, name='orderindeliverydetails'),
    path('billorderbyadmin/', adminpanelview.billorderbyadmin, name='billorderbyadmin'),
    path('cancelorderbyadmin/', adminpanelview.cancelorderbyadmin, name='cancelorderbyadmin'),
    path('deliveredorderdetails/', adminpanelview.deliveredorderdetails, name='deliveredorderdetails'),
    path('cancelledorderdetails/', adminpanelview.cancelledorderdetails, name='cancelledorderdetails'),
    path('banners/', adminpanelview.banners, name='banners'),
    path('companydetails/', adminpanelview.companydetails, name='companydetails'),

]