__author__ = 'FARID ILHAM Al-Q'

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from Apps.Distribution.CRM.models import Contacts, News, Complaint
from Apps.Distribution.CRM.forms import ContactForm, ComplaintForm
from Apps.Inventory.product.models import Category
from django.contrib.auth.decorators import login_required


def contact_info(request):
    data = Category.objects.all()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            kontak = Contacts(name=form.cleaned_data['name'], email=form.cleaned_data['email'],
                              phone=form.cleaned_data['phone'],
                              company=form.cleaned_data['company'],
                              country=form.cleaned_data['country'],
                              referral=form.cleaned_data['referral'],
                              comment=form.cleaned_data['comment'],
            )
            human = True
            kontak.save()
            #messages.add_message(request, messages.INFO, 'Your message has been sent. Thank you.')
            return render_to_response('pages/contacts_success.html', {'item': data}, context_instance=RequestContext(request))
    else:
        form = ContactForm()

    return render_to_response('pages/contacts.html', {'item': data, 'form':form}, context_instance=RequestContext(request))


def newspage(request):
    data = Category.objects.all()
    berita = News.objects.all()
    ctx = {'berita': berita, 'item': data}
    return render_to_response('pages/news.html', ctx, context_instance=RequestContext(request))


def complaint_success(request):
    return render_to_response('pages/complaint_success.html', context_instance=RequestContext(request))


@login_required
def complaint(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login')
    profiles = request.user.get_profile()
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES,)
        if form.is_valid():
            komplain = Complaint(customer=form.cleaned_data['customer'], about=form.cleaned_data['about'],
                                 description=form.cleaned_data['description'],
            )
            human = True
            komplain.save()
            return HttpResponseRedirect('/about/complaint_success')
            #messages.add_message(request, messages.INFO, 'Your message has been sent. Thank you.')

    else:
        form = ComplaintForm({'customer': profiles})

    return render_to_response('pages/complaint.html', {'form':form}, context_instance=RequestContext(request))
