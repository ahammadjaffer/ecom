from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address1 = models.TextField(max_length=500, blank=True, null=True)
    address2 = models.TextField(max_length=500, blank=True, null=True)
    phonenumber = models.IntegerField(blank=True, null=True)
    pincode = models.CharField(max_length=200, blank=True, null=True)
    addeddate = models.DateTimeField(auto_now=True)
    enddate = models.DateTimeField(auto_now=False, null=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Products(models.Model):
    name = models.CharField(max_length=200, null=False)
    description = models.CharField(max_length=1000, null=False)
    categoryid = models.IntegerField(blank=False, null=False)
    count = models.IntegerField(blank=False, null=False)
    price = models.IntegerField(blank=False, null=False)
    tax = models.IntegerField(blank=True, null=True)
    sellerid = models.IntegerField(blank=False, null=False)
    addeddate = models.DateTimeField(auto_now=True)
    enddate = models.DateTimeField(auto_now=False, null=True)
    status = models.IntegerField(blank=False, null=False)
    discount = models.IntegerField(blank=True, null=True)
    shipmentcharge = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.name

class ProductImages(models.Model):
    productid = models.ForeignKey(Products, on_delete=models.CASCADE)
    productImage = models.ImageField(upload_to='productimages/', blank=True, null=True)

    @property
    def imageURL(self):
        try:
            url = self.productImage.url
        except:
            url = ''
        return url

class Category(models.Model):
    name = models.CharField(max_length=200, null=False)
    addeddate = models.DateTimeField(auto_now=True)
    enddate = models.DateTimeField(auto_now=False, null=True)
    status = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.name

class Order(models.Model):
    orderid = models.CharField(max_length=50, null=False)
    clientid = models.ForeignKey(User, on_delete=models.CASCADE)
    grandtotal = models.IntegerField(blank=False, null=False)
    orderdate = models.DateTimeField(auto_now=True)
    enddate = models.DateTimeField(auto_now=False, null=True)
    billeddate = models.DateTimeField(auto_now=False, null=True)
    status = models.IntegerField(blank=False, null=False)
    isfulfilled = models.IntegerField(blank=False, null=False)
    isdeleted =  models.IntegerField(blank=False, null=False)
    paymentmode =  models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.orderid
    
class OrderDetails(models.Model):
    orderid = models.ForeignKey(Order, on_delete=models.CASCADE)
    productid = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False, null=False)
    producttotal = models.IntegerField(blank=False, null=False)
    addeddate = models.DateTimeField(auto_now=True)
    