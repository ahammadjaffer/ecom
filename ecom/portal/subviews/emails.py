from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from . import portalview
from ecom.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

def ordermade(request, userid):
    ordermadeclient(request, userid)
    ordermadeshop(request)
    return True

def ordercancelled(request, userid):
    ordercancelledclient(request, userid)
    ordercancelledshop(request)
    return True

# send email to client when order is made
def ordermadeclient(request, userid):
    # get client details
    clientdetail = User.objects.filter(id=userid)[0]
    sendto = clientdetail.email
    # set email body
    emailsubject = "Order succesfully placed"
    emailbody = "Order succesfully placed."
    sendemail(request, sendto, emailsubject, emailbody)

# send email to shop when order is made
def ordermadeshop(request):
    # get shop details
    sendto = EMAIL_HOST_USER
    # set email body
    emailsubject = "New order notification"
    emailbody = "New order notification."
    sendemail(request, sendto, emailsubject, emailbody)

# send email to client when order is cancelled
def ordercancelledclient(request, userid):
    # get client details
    clientdetail = User.objects.filter(id=userid)[0]
    sendto = clientdetail.email
    # set email body
    emailsubject = "Order cancellation notification"
    emailbody = "Your order cancelled"
    sendemail(request, sendto, emailsubject, emailbody)

# send email to shop when order is cancelled
def ordercancelledshop(request):
    # get shop details
    sendto = EMAIL_HOST_USER
    # set email body
    emailsubject = "Order cancellation notification"
    emailbody = "Client cancelled order"
    sendemail(request, sendto, emailsubject, emailbody)

def sendemail(request, sendto, emailsubject, emailbody):
    msg = EmailMultiAlternatives(emailsubject, emailbody, EMAIL_HOST_USER, [sendto])
    msg.attach_alternative(emailbody, "text/html")
    msg.send()