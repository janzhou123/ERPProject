from django.shortcuts import render, get_object_or_404, render_to_response, HttpResponse
from Apps.Procurement.vendor.models import *
from Apps.Procurement.internal.models import *
from Apps.Procurement.publicTender.models import *
from Apps.Procurement.directAppointment.models import *
from Apps.Procurement.purchaseOrder.models import *
from Apps.Procurement.goodsReceipt.models import *

from Apps.Accounting.CashBank.models import Budget
from Apps.Accounting.GeneralLedger.models import Ms_Fiscal_Years
from Apps.Hrm.Master_General.models import Department

from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.core.paginator import *
from Apps.Procurement.forms import *
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from filetransfers.api import prepare_upload, serve_file

def index(request):
    # get the vendor posts that are published
    posts = Announcement_Proc.objects.filter(published=True).order_by('-proc_add_date')
    paginator = Paginator(posts, 5) # Show 5 post per page
    page = request.GET.get('page')
    try:
        postx = paginator.page(page)
    except PageNotAnInteger:
        postx = paginator.page(1)
    except EmptyPage:
        postx = paginator.page(paginator.num_pages)
    uname = ''
    try :
        level = request.session['level']
        uname = request.session['uname']
    except:
        level = ''
        pass
    if level == '':
        isimenu = 'login'
    elif level == 'vendor':
        isimenu = 'vendor'
    else :
        isimenu = 'staff'
    # now return the rendered template
    return render(request, 'templatesproc/vendor/index.html', {'posts': posts,'postx': postx, 'isimenu':isimenu, 'uname':uname})

def dashboard(request):
    try :
        level = request.session['level']
        uname = request.session['uname']
    except:
        level = ''
        pass
    if level == 'vendor':
        return render(request, 'templatesproc/vendor/dashboard.html', {'uname':uname})
    else:
        return render(request, 'templatesproc/vendor/login_required.html')

# ============================================= Start of informasi umum =========================================== #

def vendor_page(request):
    try :
        level = request.session['level']
    except:
        level = ''
        pass
    if level == 'vendor':
        isimenu = 'vendor'
        member_id = request.session['member_id']
        m = Ms_Vendor.objects.get(id=request.session['member_id'])
        s = Siup_Vendor.objects.filter(ms_vendor_id=member_id)
        i = Iujk_Vendor.objects.filter(ms_vendor_id=member_id)
        a = Apbu_Vendor.objects.filter(ms_vendor_id=member_id)
        #doc = Documents_Vendor.objects.filter(ms_vendor_id=member_id)
        doc = get_object_or_404(Documents_Vendor,ms_vendor_id=member_id)
        #request.session['uname'] = m.username
        #request.session['name'] = m.vendor_name
        #request.session['verified'] = m.vendor_verified
        #request.session['level'] = 'vendor'
        uname = request.session['uname']
        n = 1
        data = siup = iujk = apbu = {}
        data = m
        iujk = i
        siup = s
        apbu = a
        ada = s.count()
        ada2 = i.count()
        ada3 = a.count()
        view_url = reverse('Apps.Procurement.vendor.views.add_direksi')
        upload_url, upload_data = prepare_upload(request, view_url)
        if request.method == 'POST':
            form = Doc_Vendor(request.POST, request.FILES, instance=doc)
            if form.is_valid():
                form.save()
                destination = 'vendor_page'
                msg1 = 'Edit data berhasil dilakukan'
                msg2 = 'Data Dokumen SIUP / IUJK / APBU Perusahaan Anda berhasil di-update'
                return render(request, 'templatesproc/vendor/edit_success.html',{'destination':destination,'msg1':msg1,'msg2':msg2})
        else:
            form = Doc_Vendor(initial={'ms_vendor_id':member_id}, instance=doc)
        return render_to_response('templatesproc/vendor/vendor_page.html',{'data':data,'siup':siup,'iujk':iujk,'apbu':apbu,'doc':doc,'ada':ada,'ada2':ada2,
                                                                           'ada3':ada3,'uname':uname,'upload_url': upload_url,'upload_data': upload_data,'form':form}, context_instance=RequestContext(request))
    else :
        return render(request, 'templatesproc/vendor/login_required.html')

def sdm_vendor(request):
    try :
        level = request.session['level']
    except:
        level = ''
        pass
    if level == 'vendor':
        isimenu = 'vendor'
        m = Ms_Vendor.objects.get(id=request.session['member_id'])
        o = Owner_Vendor.objects.filter(ms_vendor_id=request.session['member_id'])
        d = Board_Of_Directors_Vendor.objects.filter(ms_vendor_id=request.session['member_id'])
        t1 = Experts_Vendor.objects.filter(ms_vendor_id=request.session['member_id'], permanent_status='tenaga_ahli_tetap')
        t2 = Experts_Vendor.objects.filter(ms_vendor_id=request.session['member_id'], permanent_status='tenaga_ahli_tidak_tetap')
        n=1
        owner = direksi = tenaga1 = tenaga2 = {}
        owner = o
        direksi = d
        tenaga1 = t1
        tenaga2 = t2
        ada5 = o.count()
        ada6 = d.count()
        tetap = t1.count()
        t_tetap = t2.count()
        return render(request,'templatesproc/vendor/sdm_vendor.html',{'owner':owner,'direksi':direksi, 'n':n,'tenaga1': tenaga1,'tenaga2':tenaga2,
                                                                      'ada5':ada5, 'ada6':ada6,'tetap':tetap,'t_tetap':t_tetap,})
    else :
        return render(request, 'templatesproc/vendor/login_required.html')

def class_vendor(request):
    try :
        level = request.session['level']
    except:
        level = ''
        pass
    if level == 'vendor':
        isimenu = 'vendor'
        m = Ms_Vendor.objects.get(id=request.session['member_id'])
        c = Classification_Vendor.objects.filter(ms_vendor_id=request.session['member_id'])
        #request.session['uname'] = m.username
        #request.session['name'] = m.vendor_name
        #request.session['verified'] = m.vendor_verified
        #request.session['level'] = 'vendor'
        uname = request.session['uname']
        n = 1
        data = clas = {}
        data = m
        clas = c
        ada4 = c.count()
        return render(request,'templatesproc/vendor/class_vendor.html',{'data':data,'clas':clas,'ada4':ada4,'uname':uname})
    else :
        return render(request, 'templatesproc/vendor/login_required.html')

def siup(request):
    try :
        level = request.session['level']
    except:
        level = ''
        pass
    if level == 'vendor':
        isimenu = 'vendor'
        uname = request.session['uname']
        member_id = request.session['member_id']
        data = 'SIUP'
        action = '/siup/'
        if request.method == 'POST':
            form = Siup(request.POST)
            if form.is_valid():
                form.save()
                destination = 'vendor_page'
                msg1 = 'Data berhasil dimasukkan'
                msg2 = 'Data SIUP Perusahaan Anda berhasil dimasukkan'
                return render(request,'templatesproc/vendor/edit_success.html',{'destination':destination,'msg1':msg1,'msg2':msg2})
        form = Siup(initial={'ms_vendor_id': member_id})

        return render_to_response('templatesproc/vendor/add_siup.html', {'form':form, 'data':data,'uname':uname,'action':action}, context_instance=RequestContext(request))
    else :
        return render(request, 'templatesproc/vendor/login_required.html')

def iujk(request):
    try :
        level = request.session['level']
    except:
        level = ''
        pass
    if level == 'vendor':
        isimenu = 'vendor'
        uname = request.session['uname']
        member_id = request.session['member_id']
        data = 'IUJK'
        action = '/iujk/'
        if request.method == 'POST':
            form = Iujk(request.POST)
            if form.is_valid():
                form.save()
                destination = 'vendor_page'
                msg1 = 'Data berhasil dimasukkan'
                msg2 = 'Data IUJK Perusahaan Anda berhasil dimasukkan'
                return render(request,'templatesproc/vendor/edit_success.html',{'destination':destination,'msg1':msg1,'msg2':msg2})
        form = Iujk(initial={'ms_vendor_id': member_id})

        return render_to_response('templatesproc/vendor/add_siup.html', {'form':form, 'data':data,'uname':uname,'action':action}, context_instance=RequestContext(request))
    else :
        return render(request, 'templatesproc/vendor/login_required.html')

def apbu(request):
    try :
        level = request.session['level']
    except:
        level = ''
        pass
    if level == 'vendor':
        isimenu = 'vendor'
        uname = request.session['uname']
        member_id = request.session['member_id']
        action = '/apbu/'
        data = 'APBU'
        if request.method == 'POST':
            form = Apbu(request.POST)
            if form.is_valid():
                form.save()
                destination = 'vendor_page'
                msg1 = 'Data berhasil dimasukkan'
                msg2 = 'Data Akta Pendirian Badan Usaha Perusahaan Anda berhasil dimasukkan'
                return render(request,'templatesproc/vendor/edit_success.html',{'destination':destination,'msg1':msg1,'msg2':msg2})
        form = Apbu(initial={'ms_vendor_id': member_id})

        return render_to_response('templatesproc/vendor/add_siup.html', {'form':form, 'data':data,'uname':uname,'action':action}, context_instance=RequestContext(request))
    else :
        return render(request, 'templatesproc/vendor/login_required.html')

def edit_siup(request):
    try :
        level = request.session['level']
    except:
        level = ''
        pass
    if level == 'vendor':
        uname = request.session['uname']
        s = get_object_or_404(Siup_Vendor,ms_vendor_id=request.session['member_id'])
        member_id = request.session['member_id']
        action = '/edit_siup/'
        data = 'SIUP'
        if request.method == 'POST':
            form = Siup(request.POST or None, instance=s)
            if form.is_valid():
                form.save()
                destination = 'vendor_page'
                msg1 = 'Edit data berhasil dilakukan'
                msg2 = 'Data SIUP Perusahaan Anda berhasil di-update'
                return render(request, 'templatesproc/vendor/edit_success.html',{'destination':destination,'msg1':msg1,'msg2':msg2})
        else:
            form =Siup(initial={'ms_vendor_id':member_id},instance=s)
        return render_to_response('templatesproc/vendor/add_siup.html', {'form':form, 'data':data,'uname':uname,'action':action}, context_instance=RequestContext(request))
    else:
        return render(request, 'templatesproc/vendor/login_required.html')

def edit_iujk(request):
    try :
        level = request.session['level']
    except:
        level = ''
        pass
    if level == 'vendor':
        uname = request.session['uname']
        i = get_object_or_404(Iujk_Vendor,ms_vendor_id=request.session['member_id'])
        member_id = request.session['member_id']
        action = '/edit_iujk/'
        data = 'IUJK'
        if request.method == 'POST':
            form = Iujk(request.POST or None, instance=i)
            if form.is_valid():
                form.save()
                destination = 'vendor_page'
                msg1 = 'Edit data berhasil dilakukan'
                msg2 = 'Data IUJK Perusahaan Anda berhasil di-update'
                return render(request, 'templatesproc/vendor/edit_success.html',{'destination':destination,'msg1':msg1,'msg2':msg2})
        else:
            form =Iujk(initial={'ms_vendor_id':member_id},instance=i)
        return render_to_response('templatesproc/vendor/add_siup.html', {'form':form, 'data':data,'uname':uname,'action':action}, context_instance=RequestContext(request))
    else:
        return render(request, 'templatesproc/vendor/login_required.html')

def edit_apbu(request):
    try :
        level = request.session['level']
    except:
        level = ''
        pass
    if level == 'vendor':
        uname = request.session['uname']
        a = get_object_or_404(Apbu_Vendor,ms_vendor_id=request.session['member_id'])
        member_id = request.session['member_id']
        action = '/edit_apbu/'
        data = 'APBU'
        if request.method == 'POST':
            form = Apbu(request.POST or None, instance=a)
            if form.is_valid():
                form.save()
                destination = 'vendor_page'
                msg1 = 'Edit data berhasil dilakukan'
                msg2 = 'Data Akta Pendirian Badan Usaha Perusahaan Anda berhasil di-update'
                return render(request, 'templatesproc/vendor/edit_success.html',{'destination':destination,'msg1':msg1,'msg2':msg2})
        else:
            form =Apbu(initial={'ms_vendor_id':member_id},instance=a)
        return render_to_response('templatesproc/vendor/add_siup.html', {'form':form, 'data':data,'uname':uname,'action':action}, context_instance=RequestContext(request))
    else:
        isimenu='staff'
        return render(request, 'templatesproc/vendor/login_required.html')

def edit_vendor(request):
    try :
        level = request.session['level']
    except:
        level = ''
        pass
    if level == 'vendor':
        m = get_object_or_404(Ms_Vendor,id=request.session['member_id'])
        if request.method == 'POST':
            form = EditData(request.POST or None, instance=m)
            if form.is_valid():
                form.save()
                destination = 'vendor_page'
                msg1 = 'Informasi umum berhasil dimasukkan'
                msg2 = 'Data informasi umum  Perusahaan Anda berhasil di-update'
                return render(request, 'templatesproc/vendor/edit_success.html',{'destination':destination,'msg1':msg1,'msg2':msg2})
        else:
            form =EditData(instance=m)
        return render_to_response('templatesproc/vendor/edit_vendor.html', {'form':form}, context_instance=RequestContext(request))
    else:
        return render(request, 'templatesproc/vendor/login_required.html')

def edit_owner(request, id):
    try :
        level = request.session['level']
    except:
        level = ''
        pass
    if level == 'vendor':
        view_url = reverse('Apps.Procurement.vendor.views.add_owner')
        upload_url, upload_data = prepare_upload(request, view_url)
        uname = request.session['uname']
        o = get_object_or_404(Owner_Vendor,id=id)
        member_id = request.session['member_id']
        action = '/edit_owner/'+id+'/'
        data = 'Pemilik'
        if request.method == 'POST':
            form = Owner(request.POST or None,request.FILES,instance=o)
            if form.is_valid():
                form.save()
                destination = 'sdm_vendor'
                msg1 = 'Data pemilik berhasil dimasukkan'
                msg2 = 'Data pemilik perusahaan Anda berhasil di-update'
                return render(request, 'templatesproc/vendor/edit_success.html',{'destination':destination,'msg1':msg1,'msg2':msg2})
        else:
            form =Owner(initial={'ms_vendor_id':member_id},instance=o)
        return render_to_response('templatesproc/vendor/add_owner.html', {'form':form, 'data':data,'uname':uname,'action':action, 'upload_url': upload_url,
                                                                          'upload_data': upload_data}, context_instance=RequestContext(request))
    else:
        isimenu='staff'
        return render(request, 'templatesproc/vendor/login_required.html')

def edit_direksi(request, id):
    try :
        level = request.session['level']
    except:
        level = ''
        pass
    if level == 'vendor':
        view_url = reverse('Apps.Procurement.vendor.views.add_direksi')
        upload_url, upload_data = prepare_upload(request, view_url)
        uname = request.session['uname']
        d = get_object_or_404(Board_Of_Directors_Vendor,id=id)
        member_id = request.session['member_id']
        action = '/edit_direksi/'+id+'/'
        data = 'Direksi'
        if request.method == 'POST':
            form = Direksi(request.POST or None, request.FILES, instance=d)
            if form.is_valid():
                form.save()
                destination = 'sdm_vendor'
                msg1 = 'Data berhasil dimasukkan'
                msg2 = 'Data direksi Perusahaan Anda berhasil di-update'
                return render(request, 'templatesproc/vendor/edit_success.html',{'destination':destination,'msg1':msg1,'msg2':msg2})
        else:
            form =Direksi(initial={'ms_vendor_id':member_id},instance=d)
        return render_to_response('templatesproc/vendor/add_owner.html', {'form':form, 'data':data,'uname':uname,'action':action, 'upload_url': upload_url,
                                                                          'upload_data': upload_data}, context_instance=RequestContext(request))
    else:
        return render(request, 'templatesproc/vendor/login_required.html')

def edit_ta(request, id):
    try :
        level = request.session['level']
    except:
        level = ''
        pass
    if level == 'vendor':
        view_url = reverse('Apps.Procurement.vendor.views.add_ta')
        upload_url, upload_data = prepare_upload(request, view_url)
        uname = request.session['uname']
        t = get_object_or_404(Experts_Vendor,id=id)
        member_id = request.session['member_id']
        action = '/edit_ta/'+id+'/'
        data = 'Tenaga Ahli'
        if request.method == 'POST':
            form = TenagaAhli(request.POST or None, request.FILES, instance=t)
            if form.is_valid():
                form.save()
                destination = 'sdm_vendor'
                msg1 = 'Data berhasil dimasukkan'
                msg2 = 'Data tenaga ahli Perusahaan Anda berhasil di-update'
                return render(request, 'templatesproc/vendor/edit_success.html',{'destination':destination,'msg1':msg1,'msg2':msg2})
        else:
            form =TenagaAhli(initial={'ms_vendor_id':member_id},instance=t)
        return render_to_response('templatesproc/vendor/add_owner.html', {'form':form, 'data':data,'uname':uname,'action':action, 'upload_url': upload_url,
                                                                          'upload_data': upload_data}, context_instance=RequestContext(request))
    else:
        return render(request, 'templatesproc/vendor/login_required.html')

def add_class(request):
    try :
        level = request.session['level']
    except:
        level = ''
        pass
    if level == 'vendor':
        uname = request.session['uname']
        member_id = request.session['member_id']
        action = '/add_class/'
        data = 'Klasifikasi'
        if request.method == 'POST':
            form = Klasifikasi(request.POST)
            if form.is_valid():
                form.save()
                destination = 'class_vendor'
                msg1 = 'Data berhasil dimasukkan'
                msg2 = 'Penambahan klasifikasi Perusahaan Anda berhasil dilakukan'
                return render(request,'templatesproc/vendor/edit_success.html',{'destination':destination,'msg1':msg1,'msg2':msg2})
        else:
            form = Klasifikasi(initial={'ms_vendor_id':member_id})
        return render_to_response('templatesproc/vendor/add_siup.html', {'form':form,'data':data, 'uname':uname,'action':action}, context_instance=RequestContext(request))
    else:
        return render(request, 'templatesproc/vendor/login_required.html')

def del_class(request, id):
    try :
        level = request.session['level']
    except:
        level = ''
        pass
    if level == 'vendor':
        isimenu = 'vendor'
        Classification_Vendor.objects.filter(id=id).delete()
        destination = 'class_vendor'
        msg1 = 'Data berhasil dihapus'
        msg2 = 'Data klasifikasi Perusahaan Anda berhasil dihapus'
        return render(request, 'templatesproc/vendor/edit_success.html',{'isimenu':isimenu,'destination':destination,'msg1':msg1,'msg2':msg2})
    else:
        return render(request, 'templatesproc/vendor/login_required.html')

def add_owner(request):
    try :
        level = request.session['level']
    except:
        level = ''
        pass
    if level == 'vendor':
        view_url = reverse('Apps.Procurement.vendor.views.add_owner')
        upload_url, upload_data = prepare_upload(request, view_url)
        uname = request.session['uname']
        member_id = request.session['member_id']
        action = '/add_owner/'
        data = 'Pemilik'
        if request.method == 'POST':
            form = Owner(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                destination = 'sdm_vendor'
                msg1 = 'Data berhasil dimasukkan'
                msg2 = 'Penambahan data Pemilik Perusahaan Anda berhasil dilakukan'
                return render(request,'templatesproc/vendor/edit_success.html',{'destination':destination,'msg1':msg1,'msg2':msg2})
        else:
            form = Owner(initial={'ms_vendor_id':member_id})
        return render_to_response('templatesproc/vendor/add_owner.html', {'form':form,'data':data, 'uname':uname,'action':action, 'upload_url': upload_url,
                                                                          'upload_data': upload_data}, context_instance=RequestContext(request))
    else:
        return render(request, 'templatesproc/vendor/login_required.html')

def download_handler(request, id):
    dok = get_object_or_404(Owner_Vendor, id=id)
    return serve_file(request, dok.doc_ownership)

def del_owner(request, id):
    try :
        level = request.session['level']
    except:
        level = ''
        pass
    if level == 'vendor':
        isimenu = 'vendor'
        Owner_Vendor.objects.filter(id=id).delete()
        destination = 'sdm_vendor'
        msg1 = 'Data berhasil dihapus'
        msg2 = 'Data pemilik Perusahaan Anda berhasil dihapus'
        return render(request, 'templatesproc/vendor/edit_success.html',{'isimenu':isimenu,'destination':destination,'msg1':msg1,'msg2':msg2})
    else:
        return render(request, 'templatesproc/vendor/login_required.html')

def add_direksi(request):
    try :
        level = request.session['level']
    except:
        level = ''
        pass
    if level == 'vendor':
        view_url = reverse('Apps.Procurement.vendor.views.add_direksi')
        upload_url, upload_data = prepare_upload(request, view_url)
        uname = request.session['uname']
        member_id = request.session['member_id']
        action = '/add_direksi/'
        data = 'Direksi'
        if request.method == 'POST':
            form = Direksi(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                destination = 'sdm_vendor'
                msg1 = 'Data berhasil dimasukkan'
                msg2 = 'Penambahan data direksi Perusahaan Anda berhasil dilakukan'
                return render(request,'templatesproc/vendor/edit_success.html',{'destination':destination,'msg1':msg1,'msg2':msg2})
        else:
            form = Direksi(initial={'ms_vendor_id':member_id})
        return render_to_response('templatesproc/vendor/add_owner.html', {'form':form,'data':data, 'uname':uname,'action':action, 'upload_url': upload_url,
                                                                          'upload_data': upload_data}, context_instance=RequestContext(request))
    else:
        return render(request, 'templatesproc/vendor/login_required.html')

def download_direksi(request, id):
    dok = get_object_or_404(Board_Of_Directors_Vendor, id=id)
    return serve_file(request, dok.doc_board_of_directors)
#return render(request, '/media/Apps/Procurement/templatesproc/vendor/%(dok)s' % {'dok':dok.doc_board_of_directors})

def del_direksi(request, id):
    try :
        level = request.session['level']
    except:
        level = ''
        pass
    if level == 'vendor':
        isimenu = 'vendor'
        Board_Of_Directors_Vendor.objects.filter(id=id).delete()
        destination = 'sdm_vendor'
        msg1 = 'Data berhasil dihapus'
        msg2 = 'Data direksi Perusahaan Anda berhasil dihapus'
        return render(request, 'templatesproc/vendor/edit_success.html',{'isimenu':isimenu,'destination':destination,'msg1':msg1,'msg2':msg2})
    else:
        return render(request, 'templatesproc/vendor/login_required.html')

def add_ta(request):
    try :
        level = request.session['level']
    except:
        level = ''
        pass
    if level == 'vendor':
        view_url = reverse('Apps.Procurement.vendor.views.add_ta')
        upload_url, upload_data = prepare_upload(request, view_url)
        uname = request.session['uname']
        member_id = request.session['member_id']
        action = '/add_ta/'
        data = 'Tenaga Ahli'
        if request.method == 'POST':
            form = TenagaAhli(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                destination = 'sdm_vendor'
                msg1 = 'Data berhasil dimasukkan'
                msg2 = 'Penambahan data tenaga ahli Perusahaan Anda berhasil dilakukan'
                return render(request,'templatesproc/vendor/edit_success.html',{'destination':destination,'msg1':msg1,'msg2':msg2})
        else:
            form = TenagaAhli(initial={'ms_vendor_id':member_id})
        return render_to_response('templatesproc/vendor/add_owner.html', {'form':form,'data':data, 'uname':uname,'action':action, 'upload_url': upload_url,
                                                                          'upload_data': upload_data}, context_instance=RequestContext(request))
    else:
        return render(request, 'templatesproc/vendor/login_required.html')

def download_ta(request, id):
    dok = get_object_or_404(Experts_Vendor, id=id)
    return serve_file(request, dok.doc_experts)

def del_ta(request, id):
    try :
        level = request.session['level']
    except:
        level = ''
        pass
    if level == 'vendor':
        isimenu = 'vendor'
        Experts_Vendor.objects.filter(id=id).delete()
        destination = 'sdm_vendor'
        msg1 = 'Data berhasil dihapus'
        msg2 = 'Data tenaga ahli Perusahaan Anda berhasil dihapus'
        return render(request, 'templatesproc/vendor/edit_success.html',{'destination':destination,'msg1':msg1,'msg2':msg2})
    else:
        return render(request, 'templatesproc/vendor/login_required.html')

# ============================================ End of informasi umum ============================================= #

# ============================================ Start of pelelangan =============================================== #
def post(request, slug): # ================ detail post index
    try :
        level = request.session['level']
        uname = request.session['uname']
    except:
        level = ''
        pass
    if level == 'vendor':
        isimenu = 'vendor'
        # get the Pengumuman_Proc object
        post = get_object_or_404(Announcement_Proc, slug=slug)
        vendor = {}
        try:
            vendor = Classification_Vendor.objects.filter(ms_vendor_id__username=uname)
            jml = vendor.count()
        except:
            jml = 0
            pass

        return render(request, 'templatesproc/vendor/post.html', {'post': post,'isimenu':isimenu, 'uname':uname})
    else:
        return render(request, 'templatesproc/vendor/login_required.html')

def post_detail(request, slug): # ================ detail post control panel
    try :
        level = request.session['level']
        uname = request.session['uname']
    except:
        level = ''
        pass
    if level == 'vendor':
        isimenu = 'vendor'
        # get the Pengumuman_Proc object
        post = get_object_or_404(Announcement_Proc, slug=slug)
        ikut = False
        try:
            follow = Vendor_Proc.objects.filter(ms_vendor__username=uname,announcement_proc__slug=slug)
            if follow.count() > 0:
                ikut = True
        except:
            pass
        vendor = {}
        try:
            vendor = Classification_Vendor.objects.filter(ms_vendor_id__username=uname)
            jml = vendor.count()
        except:
            jml = 0
            pass
        blhAkses = False

        if jml > 0:
            for ven in vendor:
                if post.classification == ven.classification_id and post.fields == ven.fields_id and post.sub_fields == ven.sub_fields_id:
                    blhAkses = True

        return render(request, 'templatesproc/vendor/post_detail.html', {'post': post,'isimenu':isimenu, 'uname':uname, 'blhAkses':blhAkses,
                                                                         'ikut':ikut,'vendor':vendor,'jml':jml})
    else:
        return render(request, 'templatesproc/vendor/login_required.html')

def add_tender(request,slug): # ================ pendaftaran
    try :
        level = request.session['level']
        uname = request.session['uname']
    except:
        level = ''
        pass
    if level == 'vendor':
        ven = Ms_Vendor.objects.get(username=uname)
        ann = Announcement_Proc.objects.get(slug=slug)
        daftar = Vendor_Proc(ms_vendor=ven, announcement_proc=ann)
        daftar.save()
        destination = 'post_detail/%(slug)s' % {'slug':slug}
        msg1 = 'Pendaftaran Berhasil Dilakukan'
        msg2 = 'Pendaftaran Perusahaan Anda dalam pelelangan berhasil dilakukan, Selamat Mengikuti'
        return render(request, 'templatesproc/vendor/edit_success.html',{'destination':destination,'msg1':msg1,'msg2':msg2})
    else:
        return render(request, 'templatesproc/vendor/login_required.html')

def bidding(request, slug): # =============== detail penawaran yang diikutin post msg
    try :
        level = request.session['level']
        uname = request.session['uname']
    except:
        level = ''
        pass
    if level == 'vendor':
        isimenu = 'vendor'
        post = get_object_or_404(Announcement_Proc, slug=slug)
        vendor = pesan = {}
        jml = bid = 0
        try:
            vendor = Vendor_Proc.objects.filter(ms_vendor__username=uname, announcement_proc__slug=slug)
            jml = vendor.count()
            ven = Vendor_Proc.objects.get(ms_vendor__username=uname, announcement_proc__slug=slug)
            pesan = Bidding_Proc.objects.filter(vendor_proc=ven).order_by('-msg_add_date')
        except:
            jml = 0
            pass
        action = '/bidding/'+slug+'/'

        if request.method == 'POST':
            msg = request.POST['msg']
            data = Bidding_Proc(vendor_proc=ven, message=msg, uname=ven.ms_vendor.username)
            data.save()

        if jml>0:
            return render(request, 'templatesproc/vendor/bidding.html', {'post': post,'isimenu':isimenu, 'uname':uname,'ven':ven,
                                                                         'action':action,'pesan':pesan})
        else:
            return render(request, 'templatesproc/vendor/not_found.html', {'post': post,'isimenu':isimenu, 'uname':uname})
    else:
        return render(request, 'templatesproc/vendor/login_required.html')

def edit_bidding(request, slug): # ================ edit value penawaran
    try :
        level = request.session['level']
    except:
        level = ''
        pass
    if level == 'vendor':
        view_url = reverse('Apps.Procurement.vendor.views.add_ta')
        upload_url, upload_data = prepare_upload(request, view_url)
        uname = request.session['uname']
        t = Vendor_Proc.objects.get(ms_vendor__username=uname, announcement_proc__slug=slug)
        member_id = request.session['member_id']
        action = '/edit_bidding/'+slug+'/'
        data = 'Penawaran'
        if request.method == 'POST':
            form = VendorProc(request.POST or None, request.FILES, instance=t)
            if form.is_valid():
                form.save()
                destination = 'bidding/%(x)s' % {'x':slug}
                msg1 = 'Penawaran Berhasil di Update'
                msg2 = 'Data penawaran pelelangan Anda berhasil dimasukkan'
                return render(request, 'templatesproc/vendor/edit_success.html',{'destination':destination,'msg1':msg1,'msg2':msg2})
        else:
            form =VendorProc(instance=t)
        return render_to_response('templatesproc/vendor/add_owner.html', {'form':form, 'data':data,'uname':uname,'action':action, 'upload_url': upload_url,
                                                                          'upload_data': upload_data}, context_instance=RequestContext(request))
    else:
        return render(request, 'templatesproc/vendor/login_required.html')

"""
def post_message(request, id):
	ven = Vendor_Proc.objects.get(id=id) 
	msg = request.POST['msg']
	data = Bidding_Proc(vendor_proc=ven, message=msg, uname=ven.ms_vendor.username)
	data.save()
	destination = 'bidding/'+ven.announcement_proc.slug
	msg1 = 'Pesan Berhasil Dikirim'
	return render(request, 'templatesproc/vendor/edit_success.html',{'destination':destination})
"""

def download_ur_doc(request, id):
    dok = get_object_or_404(Vendor_Proc, id=id)
    return serve_file(request, dok.doc_bid)

def list_proc(request,id):
    try :
        level = request.session['level']
        uname = request.session['uname']
    except:
        level = ''
        pass
    if level == 'vendor':
        c = Classification.objects.all()
        f = Fields.objects.all()
        s = Sub_Fields.objects.all()
        posts = {}
        enter = False
        k = b = sb = key = ''
        if request.method=='POST' or id=='2':
            try:
                if request.POST['com_class']=='Klasifikasi -':
                    k = ''
                else:
                    k = request.POST['com_class']
                if request.POST['com_fields']=='Bidang -':
                    b = ''
                else:
                    b = request.POST['com_fields']
                if request.POST['com_sub']=='Sub Bidang -':
                    sb = ''
                else:
                    sb = request.POST['com_sub']
                if request.POST['keyword']=='Keyword' or request.POST['keyword']=='':
                    key = ''
                else:
                    key = request.POST['keyword']
            except:
                key = request.session['key']
                k = request.session['k']
                b = request.session['b']
                sb = request.session['sb']
            request.session['key'] = key
            request.session['k'] = k
            request.session['b'] = b
            request.session['sb'] = sb
            enter = True
            posts = Announcement_Proc.objects.filter(title__contains=key,classification__classification_detail__contains=k, published=True,
                                                     fields__fields_detail__contains=b, sub_fields__sub_fields_detail__contains=sb).order_by('-proc_add_date')
            n = posts.count()
        if id == '1':
            posts = Announcement_Proc.objects.filter(published=True).order_by('-proc_add_date')
            n = posts.count()
        paginator = Paginator(posts, 10) # Show 5 post per page
        page = request.GET.get('page')
        try:
            postx = paginator.page(page)
        except PageNotAnInteger:
            postx = paginator.page(1)
        except EmptyPage:
            postx = paginator.page(paginator.num_pages)
        return render(request, 'templatesproc/vendor/list_proc.html',{'postx':postx,'uname':uname,'n':n,'c':c,'f':f,'s':s, 'enter':enter,
                                                                      'key':key,'k':k,'b':b,'sb':sb})
    else:
        return render(request, 'templatesproc/vendor/login_required.html')

def list_reg_proc(request,id):
    try :
        level = request.session['level']
        uname = request.session['uname']
    except:
        level = ''
        pass
    if level == 'vendor':
        posts = {}
        jml=0
        c = Classification.objects.all()
        f = Fields.objects.all()
        s = Sub_Fields.objects.all()
        enter = False
        k = b = sb = key = ''
        if request.method=='POST' or id=='2':
            try:
                if request.POST['com_class']=='Klasifikasi -':
                    k = ''
                else:
                    k = request.POST['com_class']
                if request.POST['com_fields']=='Bidang -':
                    b = ''
                else:
                    b = request.POST['com_fields']
                if request.POST['com_sub']=='Sub Bidang -':
                    sb = ''
                else:
                    sb = request.POST['com_sub']
                if request.POST['keyword']=='Keyword' or request.POST['keyword']=='':
                    key = ''
                else:
                    key = request.POST['keyword']
            except:
                key = request.session['key']
                k = request.session['k']
                b = request.session['b']
                sb = request.session['sb']
            request.session['key'] = key
            request.session['k'] = k
            request.session['b'] = b
            request.session['sb'] = sb
            enter = True
            posts = Vendor_Proc.objects.filter(announcement_proc__title__contains=key,announcement_proc__classification__classification_detail__contains=k,
                                               announcement_proc__fields__fields_detail__contains=b, announcement_proc__sub_fields__sub_fields_detail__contains=sb)
            jml = posts.count()
        if id == '1':
            try:
                posts = Vendor_Proc.objects.filter(ms_vendor__username=uname).order_by('-announcement_proc__proc_add_date')
                jml = posts.count()
            except:
                pass
        paginator = Paginator(posts, 10) # Show 5 post per page
        page = request.GET.get('page')
        try:
            postx = paginator.page(page)
        except PageNotAnInteger:
            postx = paginator.page(1)
        except EmptyPage:
            postx = paginator.page(paginator.num_pages)
        return render(request, 'templatesproc/vendor/list_reg_proc.html',{'postx':postx,'uname':uname,'jml':jml,'c':c,'f':f,'s':s, 'enter':enter,
                                                                          'key':key,'k':k,'b':b,'sb':sb})
    else:
        return render(request, 'templatesproc/vendor/login_required.html')
# ===================================================== END of pelelangan ========================================================== #

# ======================================================= Start of Inbox =========================================================== #
def bid_inbox(request): # ================== inbox permintaan penawaran
    try :
        level = request.session['level']
        uname = request.session['uname']
    except:
        level = ''
        pass
    if level == 'vendor':
        posts = {}
        jml=0
        try:
            posts = Bidding_Request.objects.filter(ms_vendor__username=uname, br_status=2).order_by('br_sent_date')
            jml = posts.count()
        except:
            pass

        paginator = Paginator(posts, 5) # Show 5 post per page
        page = request.GET.get('page')
        try:
            postx = paginator.page(page)
        except PageNotAnInteger:
            postx = paginator.page(1)
        except EmptyPage:
            postx = paginator.page(paginator.num_pages)
        return render(request, 'templatesproc/vendor/bid_inbox.html',{'postx':postx,'uname':uname,'jml':jml})
    else:
        return render(request, 'templatesproc/vendor/login_required.html')

def bid_detail(request, id): # ================ detail permintaan penawaran
    try :
        level = request.session['level']
        uname = request.session['uname']
    except:
        level = ''
        pass
    if level == 'vendor':
        post = get_object_or_404(Bidding_Request, id=id)
        jml = 0
        try:
            item = Bidding_Request_Item.objects.filter(bidding_request__id=id)
            jml = item.count()
        except:
            pass

        return render(request, 'templatesproc/vendor/bid_detail.html',{'post':post,'item':item,'uname':uname,'jml':jml})
    else:
        return render(request, 'templatesproc/vendor/login_required.html')

def post_bidding(request, id):
    b = Bidding_Request.objects.get(id=id)
    val = request.POST['val']
    msg = request.POST['msg']
    if val == '' or val == 'Nilai Penawaran (Rp)':
        if msg == '' or msg == 'Pesan':
            data = Bidding_Request(id=b.id, ms_vendor=b.ms_vendor, br_detail=b.br_detail, br_end_date=b.br_end_date, br_add_date=b.br_add_date,
                                   br_sent_date=b.br_sent_date,br_status=b.br_status,bid_value=b.bid_value,br_message=b.br_message)
        else:
            data = Bidding_Request(id=b.id, ms_vendor=b.ms_vendor, br_detail=b.br_detail, br_end_date=b.br_end_date, br_add_date=b.br_add_date,
                                   br_sent_date=b.br_sent_date,br_status=b.br_status,bid_value=b.bid_value,br_message=msg)
    else:
        if msg == '' or msg == 'Pesan':
            data = Bidding_Request(id=b.id, ms_vendor=b.ms_vendor, br_detail=b.br_detail, br_end_date=b.br_end_date, br_add_date=b.br_add_date,
                                   br_sent_date=b.br_sent_date,br_status=b.br_status,bid_value=float(val),br_message=b.br_message)
        else:
            data = Bidding_Request(id=b.id, ms_vendor=b.ms_vendor, br_detail=b.br_detail, br_end_date=b.br_end_date, br_add_date=b.br_add_date,
                                   br_sent_date=b.br_sent_date,br_status=b.br_status,bid_value=float(val),br_message=msg)

    data.save()
    destination = 'bid_detail/%(b)s' % {'b':b.id}
    msg1 = 'Pesan dan Nilai Penawaran Anda Berhasil Dikirim'
    return render(request, 'templatesproc/vendor/edit_success.html',{'destination':destination})

def po_inbox(request): # ================== inbox po
    try :
        level = request.session['level']
        uname = request.session['uname']
    except:
        level = ''
        pass
    if level == 'vendor':
        post = {}
        jml=0
        try:
            post = Purchase_Order.objects.filter(vendor__username=uname, po_status__startswith=2).order_by('-po_date_sent')
            jml = post.count()
        except:
            pass

        paginator = Paginator(post, 10) # Show 5 post per page
        page = request.GET.get('page')
        try:
            postx = paginator.page(page)
        except PageNotAnInteger:
            postx = paginator.page(1)
        except EmptyPage:
            postx = paginator.page(paginator.num_pages)
        return render(request, 'templatesproc/vendor/po_inbox.html',{'postx':postx,'uname':uname,'jml':jml})
    else:
        return render(request, 'templatesproc/vendor/login_required.html')

def po_detail(request, id): # ================ detail permintaan penawaran
    try :
        level = request.session['level']
        uname = request.session['uname']
    except:
        level = ''
        pass
    if level == 'vendor':
        jml = total = 0
        post = get_object_or_404(Purchase_Order, id=id)
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
        return render(request, 'templatesproc/vendor/po_detail.html',{'post':post,'item_pp':item_pp,'item_ro':item_ro,'uname':uname,'jml':jml,'total':total})
    else:
        return render(request, 'templatesproc/vendor/login_required.html')

def print_po(request, id):
    try :
        level = request.session['level']
        uname = request.session['uname']
    except:
        level = ''
        pass
    if level == 'vendor':
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
        return render(request, 'templatesproc/report/po.html', {'data':data,'item_pp':item_pp,'item_ro':item_ro,'uname':uname,'jml':jml,'total':total})
    else:
        return render(request, 'templatesproc/vendor/login_required.html')

def print_rq(request, id):
    try :
        level = request.session['level']
        uname = request.session['uname']
    except:
        level = ''
        pass
    if level == 'vendor':
        data = get_object_or_404(Bidding_Request, id=id)
        jml = 0
        try:
            item = Bidding_Request_Item.objects.filter(bidding_request__id=id)
            jml = item.count()
        except:
            pass
        return render(request, 'templatesproc/report/rq.html', {'uname':uname,'data':data,'item':item,'jml':jml})
    else:
        return render(request, 'templatesproc/vendor/login_required.html')

def claim_inbox(request): # ================== inbox po
    try :
        level = request.session['level']
        uname = request.session['uname']
    except:
        level = ''
        pass
    if level == 'vendor':
        c = {}
        jml=0
        try:
            c = Claim.objects.filter(goods_receipt_id__purchase_order_id__vendor__username=uname, claim_status=2).order_by('-claim_sent_date')
            jml = c.count()
        except:
            pass
        paginator = Paginator(c, 5) # Show 5 post per page
        page = request.GET.get('page')
        try:
            postx = paginator.page(page)
        except PageNotAnInteger:
            postx = paginator.page(1)
        except EmptyPage:
            postx = paginator.page(paginator.num_pages)
        return render(request, 'templatesproc/vendor/claim_inbox.html',{'postx':postx,'uname':uname,'jml':jml})
    else:
        return render(request, 'templatesproc/vendor/login_required.html')

def claim_detail(request, id): # ================ detail permintaan penawaran
    try :
        level = request.session['level']
        uname = request.session['uname']
    except:
        level = ''
        pass
    if level == 'vendor':
        post = get_object_or_404(Claim, id=id)
        return render(request, 'templatesproc/vendor/claim_detail.html',{'post':post,'uname':uname})
    else:
        return render(request, 'templatesproc/vendor/login_required.html')
# ======================================================= END of Inbox ============================================================= #

# ===================================================== Start of Session =========================================================== #
def register(request):
    """my register"""
    isimenu = 'home'
    if request.method == 'POST':
        form = Register(request.POST, request.FILES)
        if form.is_valid():
            member = form.save()
            return render(request,'templatesproc/vendor/reg_success.html')
    else:
        form = Register()
    return render_to_response('templatesproc/vendor/registration_form.html', {'form':form,'isimenu':isimenu}, context_instance=RequestContext(request))

def login_user(request):
    #logout(request)
    username = password = ''
    error1=''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                username = User.objects.filter(username=username, password=password)
                # Redirect to a success page.
                idusername = request.session['username'] = username
                error1=''
                return render_to_response('templatesproc/vendor/index.html',{'idusername':username}, context_instance=RequestContext(request))
            else:
                error1 = '1'
                success="<html>tidak aktif</html>"
            # Return a 'disabled account' error message
        else:
            error1 = '1'
            success="<html>Gak ada</html>"
        # Return an 'invalid login' error message.
    else :
        render(request, 'templatesproc/vendor/login.html')
    return render_to_response('templatesproc/vendor/login.html',{'error1':error1}, context_instance=RequestContext(request))

def loginsession(request):
    isimenu = 'home'
    if request.method == 'POST':
        try:
            m = Ms_Vendor.objects.get(username=request.POST['username'])
            if m.password == request.POST['password'] and m.vendor_verified == True:
                request.session['member_id'] = m.id
                request.session['uname'] = m.username
                request.session['name'] = m.vendor_name
                request.session['verified'] = m.vendor_verified
                request.session['level'] = 'vendor'
                return render(request, 'templatesproc/vendor/login_success.html',{'m':m})
            else:
                return render(request, 'templatesproc/vendor/login_not_success.html')
        except:
            try:
                u = User_Intern.objects.get(username=request.POST['username'])
                if u.password == request.POST['password'] and u.intern_verified == True:
                    request.session['level'] = u.access_level
                    request.session['member_id'] = u.id
                    request.session['uname'] = u.username
                    request.session['name'] = u.intern_name
                    request.session['verified'] = u.intern_verified
                    return render(request, 'templatesproc/vendor/login_success.html',{'u':u})
                else:
                    return render(request, 'templatesproc/vendor/login_not_success.html')
            except:
                return render(request, 'templatesproc/vendor/login_not_success.html')
                pass
    else :
        return render(request, 'templatesproc/vendor/login.html', {'isimenu':isimenu})
    return render(request, 'templatesproc/vendor/login.html')

def logoutsession(request):
    try:
        del request.session['level']
        del request.session['member_id']
        del request.session['uname']
        del request.session['name']
        del request.session['verified']
    except KeyError:
        pass
    return render(request,'templatesproc/vendor/logged_out.html')

# ============================================================== END of Session ================================================= #
