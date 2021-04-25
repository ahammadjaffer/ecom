from django.db import connection
from portal.models import *

def sitedetails(request):
    data={}
    row = Companydetails.objects.all()
    for col in row:
        data['companydetails'] = col
    data['categories'] = Category.objects.filter(status=1).values()
    data['subcategories'] = SubCategory.objects.filter(status=1).values()

    # user cart detail
    data['cartcount'] = 0
    if request.user.is_authenticated:
        user = request.user
        if (not request.user.is_superuser):
            with connection.cursor() as cursor:
                cursor.execute("select count(od.productid_id) as productcount from portal_order o left join portal_orderdetails od on o.id = od.orderid_id where o.clientid_id=%s and o.status=%s", [user.id, 0])
                row = cursor.fetchone()
                data['cartcount'] = row[0] if (row != '') else 0
    return {'companydetails':data}