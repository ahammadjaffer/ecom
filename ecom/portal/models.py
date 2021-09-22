from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.files.storage import FileSystemStorage

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    housename = models.TextField(max_length=500, blank=True, null=True)
    street = models.TextField(max_length=500, blank=True, null=True)
    landmark = models.TextField(max_length=500, blank=True, null=True)
    state = models.TextField(max_length=500, blank=True, null=True)
    country = models.TextField(max_length=500, blank=True, null=True)
    address2 = models.TextField(max_length=500, blank=True, null=True)
    phonenumber = models.CharField(max_length=13, blank=True, null=True)
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
    features = models.TextField(max_length=max, blank=True)
    deliverydetails = models.TextField(max_length=max, blank=True)
    categoryid = models.IntegerField(blank=False, null=False)
    subcategoryid = models.IntegerField(blank=False, null=False)
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

class SubCategory(models.Model):
    parentcategory = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=False)
    addeddate = models.DateTimeField(auto_now=True)
    enddate = models.DateTimeField(auto_now=False, null=True)
    status = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.name

class Order(models.Model):
    orderid = models.CharField(max_length=50, null=True)
    clientid = models.ForeignKey(User, on_delete=models.CASCADE)
    grandtotal = models.IntegerField(blank=False, null=False)
    orderdate = models.DateTimeField(auto_now=True)
    enddate = models.DateTimeField(auto_now=False, null=True)
    billeddate = models.DateTimeField(auto_now=False, null=True)
    orderaccepteddate = models.DateTimeField(auto_now=False, null=True)
    updateddate = models.DateTimeField(auto_now=False, null=True)
    status = models.IntegerField(blank=False, null=False)
    isfulfilled = models.IntegerField(blank=True, null=True)
    isdeleted =  models.IntegerField(blank=True, null=True)
    paymentmode =  models.IntegerField(blank=True, null=True)
    paymentstatus = models.IntegerField(blank=False, null=False)
    deliveredaddress = models.TextField(max_length=500, blank=True, null=True)
    
class OrderDetails(models.Model):
    orderid = models.ForeignKey(Order, on_delete=models.CASCADE)
    productid = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False, null=False)
    producttotal = models.IntegerField(blank=False, null=False)
    addeddate = models.DateTimeField(auto_now=True)
    updateddate = models.DateTimeField(auto_now=False, null=True)
    status = models.IntegerField(blank=False, null=False)
    
class Banners(models.Model):
    # t1-top banner 1, t2- top banner 2, t3-top banner 3, b1-bottom banner 1, b2-bottom banner 2, b3-bottom banner 3
    bannertag = models.CharField(max_length=5, blank=False, null=False)
    bannerimage = models.ImageField(upload_to='images/', blank=True, null=True)

    @property
    def imageURL(self):
        try:
            url = self.bannerimage.url
        except:
            url = ''
        return url

class Companydetails(models.Model):
    companytag = models.CharField(max_length=5, blank=False, null=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    address = models.TextField(max_length=500, blank=True, null=True)
    email = models.CharField(max_length=255, blank=False, null=False)
    phonenumber = models.CharField(max_length=13, blank=False, null=False)
    termsandconditions = models.TextField(max_length=max, blank=True, null=True)
    facebook = models.CharField(max_length=255, blank=False, null=False)
    instagram = models.CharField(max_length=255, blank=False, null=False)
    youtube = models.CharField(max_length=255, blank=False, null=False)
    companylogo = models.ImageField(upload_to='images/', blank=True, null=True)

    @property
    def imageURL(self):
        try:
            url = self.companylogo.url
        except:
            url = ''
        return url

class Zipcodes(models.Model):
    zipcode = models.CharField(max_length=50, null=False)
    addeddate = models.DateTimeField(auto_now=False, null=False)
    enddate = models.DateTimeField(auto_now=False, null=True)
    status = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.zipcode