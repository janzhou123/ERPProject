from Apps.Procurement.internal.models import *
from Apps.Procurement.purchaseOrder.models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

# Create your views here.
@login_required
def print_po_admin(request, id):
    jml = total = 0
    data = Purchase_Order.objects.get(id=id)
    item_pp = item_ro = {}
    try:
        item_pp = Data_Purchase_Request.objects.filter(no_po__id=id)
        jml += item_pp.count()
        for i in item_pp: total += i.request_total_price
    except:
        pass

    try:
        item_ro = Data_Rush_Order.objects.filter(no_po__id=id)
        jml += item_ro.count()
        for i in item_ro: total += i.ro_total_price
    except:
        pass
    totaltok = ppn10 = totalexp = 0
    totaltok = data.total_()
    ppn10 = data.ppn10()
    totalexp = data.total_expenditure()
    return render(request, 'templatesproc/report/po.html', {'data':data,'item_pp':item_pp,'item_ro':item_ro,'jml':jml,'total':total, 'totaltok':totaltok,'ppn10':ppn10,'totalexp':total_exp})
