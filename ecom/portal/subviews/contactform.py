from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from . import portalview
from ecom.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

def contactindex(request):
    context = {}
    return render(request, 'portal/contact.html', context)

def sendemail(request):
    try:
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        recepient = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        message =message+'''
        from '''+firstname+' '+lastname

        # send_mail(subject, body, EMAIL_HOST_USER, [recepient], fail_silently = False)
        msg = EmailMultiAlternatives(subject, message, EMAIL_HOST_USER, [recepient])
        msg.attach_alternative(message, "text/html")
        msg.send()
        messages.success(request, "Mail send successfully")
    except Exception as e:
        messages.error(request, "Error: Message send failed. Reason:- "+str(e))
    finally:
        return redirect('/contactindex')