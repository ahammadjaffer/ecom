from django.urls import path

from . import views
from .subviews import adminview

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('adminhome/', adminview.admin_home, name='admin_home'),
    path('adminprofile/', adminview.admin_profile, name='admin_profile'),
    path('changepassword/', adminview.changepassword, name='changepassword'),
    path('adminlist/', adminview.adminlist, name='adminlist'),
    path('productlist/', adminview.productlist, name='productlist'),
    path('productcategory/', adminview.productcategory, name='productcategory'),
    path('loadproductmodal/', adminview.loadproductmodal, name='loadproductmodal'),
    path('updateproduct/', adminview.updateproduct, name='updateproduct'),
    path('deleteproduct/', adminview.deleteproduct, name='deleteproduct'),
    path('updatecategory/', adminview.updatecategory, name='updatecategory'),
    path('deletecategory/', adminview.deletecategory, name='deletecategory'),
    path('manageorders/', adminview.manageorders, name='manageorders'),
    path('pendingorders/', adminview.pendingorders, name='pendingorders'),
    path('ordersindelivery/', adminview.ordersindelivery, name='ordersindelivery'),
    path('deliveredorders/', adminview.deliveredorders, name='deliveredorders'),
    path('cancelledorders/', adminview.cancelledorders, name='cancelledorders'),
    path('pendingorderdetails/', adminview.pendingorderdetails, name='pendingorderdetails'),
    path('acceptpendingorder/', adminview.acceptpendingorder, name='acceptpendingorder'),
    path('orderindeliverydetails/', adminview.orderindeliverydetails, name='orderindeliverydetails'),
    path('billorderbyadmin/', adminview.billorderbyadmin, name='billorderbyadmin'),
    path('cancelorderbyadmin/', adminview.cancelorderbyadmin, name='cancelorderbyadmin'),
    path('deliveredorderdetails/', adminview.deliveredorderdetails, name='deliveredorderdetails'),
    path('cancelledorderdetails/', adminview.cancelledorderdetails, name='cancelledorderdetails'),

]