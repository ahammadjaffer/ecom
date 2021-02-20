from portal.models import *

def sitedetails(request):
    data={}
    row = Companydetails.objects.all()
    for col in row:
        data['companydetails'] = col
    data['categories'] = Category.objects.filter(status=1).values()
    data['subcategories'] = SubCategory.objects.filter(status=1).values()
    return {'companydetails':data}