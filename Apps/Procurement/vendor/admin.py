from django.contrib import admin
from Apps.Procurement.vendor.models import *
from Apps.Procurement.internal.models import *
from Apps.Procurement.property.models import *
from Apps.Procurement.purchaseOrder.models import *
from Apps.Procurement.publicTender.models import *
from Apps.Procurement.directAppointment.models import *
from Apps.Procurement.goodsReceipt.models import *

from Apps.Accounting.CashBank.models import Budget
from Apps.Accounting.GeneralLedger.models import Ms_Fiscal_Years

from django import forms
from django.db.models import Sum
from django.contrib.admin.views.main import ChangeList
from django.contrib.contenttypes import generic
from django.forms.models import BaseInlineFormSet
from admin_decorators import allow_tags
from django.contrib.auth.models import Group

class TotalChangeList(ChangeList):
    #provide the list of fields that we need to calculate averages and totals
    fields_to_total = ['id','request_amount','request_total_price',]

    def get_total_values(self, queryset):
        """
        Get the totals
        """
        #basically the total parameter is an empty instance of the given model
        total =  Data_Purchase_Request()
        total.custom_alias_name = "Totals" #the label for the totals row
        total.request_amount = queryset.aggregate(Sum('request_amount'))
        return total
    def get_results(self, request):
        """
        The model admin gets queryset results from this method
        and then displays it in the template
        """
        super(TotalChangeList, self).get_results(request)
        #first get the totals from the current changelist
        total = self.get_total_values(self.query_set)
        total.request_amount = '{'+str(total.request_amount)[24:]
        total.request_total_price = '{Rp '+str(total.request_total_price)[28:]
        total.id = 'Total'
        #small hack. in order to get the objects loaded we need to call for
        #queryset results once so simple len function does it
        len(self.result_list)
        #and finally we add our custom rows to the resulting changelist
        self.result_list._result_cache.append(total)

class VendorProcInline(admin.TabularInline):
    model = Vendor_Proc
    extra = 0
    max_num = 0
    editable = []
    readonly_fields = ('id','ms_vendor','announcement_proc','bid_value','doc_bid')

class BiddingProcInline(admin.TabularInline):
    model = Bidding_Proc
    extra = 0
    can_delete = False
    ordering = ("-msg_add_date",)
    #readonly_fields = ('uname','msg_add_date',)
    """
    def get_formsets(self, request, obj=None):
        formset = inline.get_formset(request, obj)
        form = formset.form
        user = Group.objects.get(user=request.user)
        form.exclude = []
        if user.name == 'pel_impor' or user.name == 'pel_lokal' or user.name == 'pel_intern':
            if getattr(obj, 'uname', None) == 'admin' or getattr(obj, 'uname', None) == None:
                form.exclude = []
            else:
                form.exclude += ['message',]
        else:
            form.exclude = ['message',]
        return form
    """
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ()
        user = Group.objects.get(user=request.user)
        if user.name == 'pel_impor' or user.name == 'pel_lokal' or user.name == 'pel_intern':
            readonly_fields += ('msg_add_date','uname','msg_add_date',)
        else:
            readonly_fields += ('vendor_proc','msg_add_date','uname','msg','message')
        if request.user.is_superuser:
            readonly_fields = ()
        return readonly_fields

class DataPPInline(admin.TabularInline):
    model = Data_Purchase_Request
    extra = 0
    max_num = 0
    can_delete = False
    fields = ('header_purchase_request_id', 'request_goods_name','goods_type_id','unit_of_measure_id', 'request_used',
              'request_amount','currency_id','request_unit_price','request_total_rupiah','request_total_price','request_detail',)
    readonly_fields =('header_purchase_request_id','request_goods_name','goods_type_id','unit_of_measure_id', 'request_used','request_amount',
                      'currency_id','request_unit_price','request_total_rupiah','request_total_price','request_detail',)

class DataROInline(admin.TabularInline):
    model = Data_Rush_Order
    extra = 0
    max_num = 0
    can_delete = False
    fields = ('header_rush_order_id', 'ro_goods_name','goods_type_id','unit_of_measure_id', 'ro_used',
              'ro_amount','currency_id','ro_unit_price','ro_total_rupiah','ro_total_price','ro_detail',)
    readonly_fields =('header_rush_order_id','ro_goods_name','goods_type_id','unit_of_measure_id', 'ro_used','ro_amount',
                      'currency_id','ro_unit_price','ro_total_rupiah','ro_total_price','ro_detail',)

class SiupInline(admin.TabularInline):
    model = Siup_Vendor
    extra = 0

    def get_readonly_fields(self, request, obj=None):
        data = Group.objects.get(user=request.user)
        readonly_fields = ()
        if data.name == 'pel_impor' or data.name == 'pel_lokal' or data.name == 'pel_intern' or data.name == 'kabag_proc':
            readonly_fields = ('siup_no','siup_valid_until','siup_institute',)
        if request.user.is_superuser:
            readonly_fields = ()
        return readonly_fields

class IujkInline(admin.TabularInline):
    model = Iujk_Vendor
    extra = 0
    def get_readonly_fields(self, request, obj=None):
        data = Group.objects.get(user=request.user)
        readonly_fields = ()
        if data.name == 'pel_impor' or data.name == 'pel_lokal' or data.name == 'pel_intern' or data.name == 'kabag_proc':
            readonly_fields = ('iujk_no','iujk_valid_until','iujk_institute',)
        if request.user.is_superuser:
            readonly_fields = ()
        return readonly_fields

class ApbuInline(admin.TabularInline):
    model = Apbu_Vendor
    extra = 0
    def get_readonly_fields(self, request, obj=None):
        data = Group.objects.get(user=request.user)
        readonly_fields = ()
        if data.name == 'pel_impor' or data.name == 'pel_lokal' or data.name == 'pel_intern' or data.name == 'kabag_proc':
            readonly_fields = ('apbu_no','apbu_valid_until','apbu_institute',)
        if request.user.is_superuser:
            readonly_fields = ()
        return readonly_fields

class ClassificationInline(admin.TabularInline):
    model = Classification_Vendor
    extra = 0
    def get_readonly_fields(self, request, obj=None):
        data = Group.objects.get(user=request.user)
        readonly_fields = ()
        if data.name == 'pel_impor' or data.name == 'pel_lokal' or data.name == 'pel_intern' or data.name == 'kabag_proc':
            readonly_fields = ('classification_id','fields_id','sub_fields_id',)
        if request.user.is_superuser:
            readonly_fields = ()
        return readonly_fields

class OwnerInline(admin.TabularInline):
    model = Owner_Vendor
    extra = 0
    def get_readonly_fields(self, request, obj=None):
        data = Group.objects.get(user=request.user)
        readonly_fields = ()
        if data.name == 'pel_impor' or data.name == 'pel_lokal' or data.name == 'pel_intern' or data.name == 'kabag_proc':
            readonly_fields = ('owner_name','owner_ktp_no','owner_address','capital_ownership','doc_ownership',)
        if request.user.is_superuser:
            readonly_fields = ()
        return readonly_fields

class DirectorsInline(admin.TabularInline):
    model = Board_Of_Directors_Vendor
    extra = 0
    def get_readonly_fields(self, request, obj=None):
        data = Group.objects.get(user=request.user)
        readonly_fields = ()
        if data.name == 'pel_impor' or data.name == 'pel_lokal' or data.name == 'pel_intern' or data.name == 'kabag_proc':
            readonly_fields = ('board_of_directors_name','board_of_directors_npwp','board_of_directors_ktp_no','board_of_directors_address',
                               'occupation','doc_board_of_directors',)
        if request.user.is_superuser:
            readonly_fields = ()
        return readonly_fields

class ExpertsInline(admin.TabularInline):
    model = Experts_Vendor
    extra = 0
    def get_readonly_fields(self, request, obj=None):
        data = Group.objects.get(user=request.user)
        readonly_fields = ()
        if data.name == 'pel_impor' or data.name == 'pel_lokal' or data.name == 'pel_intern' or data.name == 'kabag_proc':
            readonly_fields = ('experts_name','experts_npwp','experts_ktp_no','experts_address','expertise','ska_no','ska_valid_until','last_education',
                               'diploma_no','permanent_status','doc_experts',)
        if request.user.is_superuser:
            readonly_fields = ()
        return readonly_fields

class ExperienceInline(admin.TabularInline):
    model = Experience_Vendor
    extra = 0
    def get_readonly_fields(self, request, obj=None):
        data = Group.objects.get(user=request.user)
        readonly_fields = ()
        if data.name == 'pel_impor' or data.name == 'pel_lokal' or data.name == 'pel_intern' or data.name == 'kabag_proc':
            readonly_fields = ('experience_user','experience_title','location','experience_address','classification_id','fields_id','sub_fields_id',
                               'experience_contract_no','experience_contract_value','experience_contract_date','doc_experience',)
        if request.user.is_superuser:
            readonly_fields = ()
        return readonly_fields

class EquipmentsInline(admin.TabularInline):
    model = Equipments_Vendor
    extra = 0
    def get_readonly_fields(self, request, obj=None):
        data = Group.objects.get(user=request.user)
        readonly_fields = ()
        if data.name == 'pel_impor' or data.name == 'pel_lokal' or data.name == 'pel_intern' or data.name == 'kabag_proc':
            readonly_fields = ('equipment_type','equipment_amount','equipment_brand','equipment_year','equipment_condition','equipment_location',
                               'evidence_no','equipment_status',)
        if request.user.is_superuser:
            readonly_fields = ()
        return readonly_fields

class DocumentsInline(admin.TabularInline):
    model = Documents_Vendor
    extra = 0
    def get_readonly_fields(self, request, obj=None):
        data = Group.objects.get(user=request.user)
        readonly_fields = ()
        if data.name == 'pel_impor' or data.name == 'pel_lokal' or data.name == 'pel_intern' or data.name == 'kabag_proc':
            readonly_fields = ('doc_siup','doc_iujk','doc_apbu',)
        if request.user.is_superuser:
            readonly_fields = ()
        return readonly_fields

class MsVendorAdmin(admin.ModelAdmin):
    list_display = ['vendor_name', 'username','vendor_npwp','date_register','vendor_phone','email','vendor_verified','grade']
    list_filter = ['vendor_verified', 'date_register']
    search_fields = ['vendor_name', 'username', 'vendor_npwp']
    date_hierarchy = 'date_register'
    save_on_top = True
    #prepopulated_fields = {"username": ("vendor_name",)}
    inlines = [SiupInline, IujkInline, ApbuInline, ClassificationInline, OwnerInline, DirectorsInline, ExpertsInline, ExperienceInline, EquipmentsInline,
               DocumentsInline,]

    def suit_row_attributes(self, obj, request):
        css_class = {
            0: 'error',
            }.get(obj.grade_rate())
        if css_class:
            return {'class':css_class, 'data':obj.grade_rate()}

    def get_readonly_fields(self, request, obj=None):
        data = Group.objects.get(user=request.user)
        readonly_fields = ()
        if data.name == 'pel_impor' or data.name == 'pel_lokal' or data.name == 'pel_intern' or data.name == 'kabag_proc':
            readonly_fields = ('vendor_name', 'username','vendor_npwp','date_register','vendor_city','fax','vendor_address','vendor_phone','email',
                               'vendor_verified','password','cp_name','cp_phone','net_worth','bank_name','bank_account_no',)
        if request.user.is_superuser:
            readonly_fields = ()
        return readonly_fields

class UserInternAdmin(admin.ModelAdmin):
    list_display = ['intern_name', 'username','intern_date_register','intern_occupation','access_level','department','intern_verified']
    list_filter = ['intern_verified']
    search_fields = ['intern_name', 'username']
    date_hierarchy = 'intern_date_register'
    save_on_top = True
    prepopulated_fields = {"username": ("intern_name",)}

class ClassificationAdmin(admin.ModelAdmin):
    list_display = ['id','classification_detail']
    save_on_top = True
    search_fields = ['classification_detail']

class FieldsAdmin(admin.ModelAdmin):
    list_display = ['id','fields_detail']
    search_fields = ['fields_detail']
    save_on_top = True

class SubFieldsAdmin(admin.ModelAdmin):
    list_display = ['id','sub_fields_detail']
    search_fields = ['sub_fields_detail']
    save_on_top = True

class SetOfDelayAdmin(admin.ModelAdmin):
    list_display = ['id','set_of_delay_detail']
    search_fields = ['set_of_delay_detail']
    save_on_top = True

class DataPlanInline(admin.TabularInline):
    model = Data_Plan
    extra = 0
    max_num = 0
    editable = []
    readonly_fields = ('id','header_plan_id','plan_goods_name','plan_used','plan_amount','goods_type_id','unit_of_measure_id','currency_id',
                       'plan_unit_price','plan_total_rupiah','plan_total_price','plan_detail')

class HeaderPlanAdmin(admin.ModelAdmin):
    list_display = ['no_reg','department', 'plan_add_date','plan_month','lock','fiscal_year']
    search_fields = ['department','no_Reg']
    save_on_top = True
    date_hierarchy = 'plan_add_date'
    list_filter = ['lock','fiscal_year__Code',]
    inlines = [DataPlanInline,]
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            readonly_fields = ()
        else:
            readonly_fields = ('id','department', 'plan_add_date','plan_month','no_reg','lock',)
        return readonly_fields

class DataPlanAdmin(admin.ModelAdmin):
    list_display = ['id','header_plan_id','plan_goods_name','plan_amount','currency_id','plan_unit_price',
                    'plan_total_rupiah','plan_total_price']
    search_fields = ['header_plan_id__no_reg','plan_goods_name']
    save_on_top = True
    list_filter = ['header_plan_id__lock',]
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            readonly_fields = ()
        else: readonly_fields = ('id','header_plan_id','plan_goods_name','plan_used','plan_amount','goods_type_id','unit_of_measure_id','currency_id',
                                 'plan_unit_price','plan_total_rupiah','plan_total_price','plan_detail',)
        return readonly_fields

class HeaderReqAdmin(admin.ModelAdmin):
    list_display = ['no_reg','header_plan','fiscal_year','department','request_lock','total_expenditure','saldo']
    search_fields = ['department__department']
    save_on_top = True
    ordering = ('-request_month', )
    list_filter = ['request_lock','header_plan__no_reg','department__department','fiscal_year__Code']
    inlines = [DataPPInline,]

    def suit_row_attributes(self, obj, request):
        user = Group.objects.get(user=request.user)
        if user.name == 'pengendali_gudang':
            css_class = {
                False: 'error',
                }.get(obj.warehouse_agreement)
            if css_class:
                return {'class':css_class, 'data':obj.warehouse_agreement}
        elif user.name == 'pengendali_financial':
            css_class = {
                False: 'error',
                }.get(obj.financial_agreement)
            if css_class:
                return {'class':css_class, 'data':obj.financial_agreement}
        elif user.name == 'pengendali_proc':
            css_class = {
                False: 'error',
                }.get(obj.procurement_agreement)
            if css_class:
                return {'class':css_class, 'data':obj.procurement_agreement}
        else:
            css_class = {
                False: 'error',
                }.get(obj.request_lock)
            if css_class:
                return {'class':css_class, 'data':obj.request_lock}

    def get_form(self, request, obj=None, **kwargs):
        form = super(HeaderReqAdmin, self).get_form(request, obj, **kwargs)
        user = Group.objects.get(user=request.user)
        self.exclude = []
        if user.name == 'pengendali_gudang':
            self.exclude += ['financial_review','procurement_review',]
            if getattr(obj, 'request_lock', None) == True:
                self.exclude += ('warehouse_review',)
        elif user.name == 'pengendali_financial':
            self.exclude += ('warehouse_review','procurement_review',)
            if getattr(obj, 'request_lock', None) == True:
                self.exclude += ('financial_review',)
        elif user.name == 'pengendali_proc':
            self.exclude += ('warehouse_review','financial_review',)
            if getattr(obj, 'request_lock', None) == True:
                self.exclude += ('procurement_review',)
        else:
            self.exclude += ('warehouse_review','financial_review','procurement_review',)

        if request.user.is_superuser:
            self.exclude = []

        return form


    def get_readonly_fields(self, request, obj=None):
        data = Group.objects.get(user=request.user)
        readonly_fields = ()
        if data.name == 'pengendali_gudang':
            readonly_fields += ('f_rev','p_rev','financial_agreement','procurement_agreement',)
            if getattr(obj, 'request_lock', None) == True:
                readonly_fields += ('w_rev','warehouse_agreement',)
        elif data.name == 'pengendali_financial':
            readonly_fields += ('w_rev','p_rev','warehouse_agreement','procurement_agreement',)
            if getattr(obj, 'request_lock', None) == True:
                readonly_fields += ('f_rev','financial_agreement',)
        elif data.name == 'pengendali_proc':
            readonly_fields += ('w_rev','f_rev','warehouse_agreement','financial_agreement',)
            if getattr(obj, 'request_lock', None) == True:
                readonly_fields += ('p_rev','procurement_agreement',)
        else:
            readonly_fields += ('w_rev','f_rev','p_rev','warehouse_agreement','financial_agreement','procurement_agreement',)

        if request.user.is_superuser:
            readonly_fields = ()
        else:
            readonly_fields += ('department','request_month','request_lock','request_lock_date','header_plan',)
        return readonly_fields

class DataReqAdmin(admin.ModelAdmin):
    list_display = ['no_item', 'header_purchase_request_id', 'request_goods_name','request_amount','currency_id','request_unit_price',
                    'request_total_rupiah','request_total_price','method_choices','state_choices','no_po']
    search_fields = ['header_purchase_request_id__id','request_goods_name']
    save_on_top = True
    list_filter = ['header_purchase_request_id__no_reg',]

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ()
        data = Group.objects.get(user=request.user)

        get = True
        po = 1
        try:
            gett = getattr(obj, 'header_purchase_request_id', None)
            get = gett.request_lock
        except:
            pass
        try:
            p = getattr(obj, 'no_po', None)
            po = p.po_status
        except:
            pass
        if get == True:
            if data.name == 'kabag_proc':
                if po == 1:
                    readonly_fields += ('method_choices','no_po','request_unit_price',)
                else: readonly_fields += ('state_choices','method_choices','no_po','request_unit_price',)
            elif data.name == 'kasi_impor' or data.name == 'kasi_lokal' or data.name == 'kasi_intern':
                if po == 1:
                    readonly_fields += ('state_choices','no_po','request_unit_price',)
                else: readonly_fields += ('state_choices','method_choices','no_po','request_unit_price',)
            elif data.name == 'pel_impor' or data.name == 'pel_lokal' or data.name == 'pel_intern':
                if po == 1:
                    readonly_fields += ('state_choices','method_choices',)
                else: readonly_fields += ('state_choices','method_choices','no_po','request_unit_price',)
            elif data.name == 'pengendali_gudang' or data.name == 'pengendali_financial' or data.name == 'pengendali_proc':
                readonly_fields += ('state_choices','method_choices','no_po','request_unit_price',)
        else:
            readonly_fields += ('state_choices','method_choices','no_po','request_unit_price',)
        if request.user.is_superuser:
            readonly_fields = ()
        else: readonly_fields += ('id', 'header_purchase_request_id', 'request_goods_name','goods_type_id','unit_of_measure_id', 'request_used',
                                  'request_amount','currency_id','request_total_rupiah','request_total_price','request_detail',)
        return readonly_fields

    def get_form(self, request, obj=None, **kwargs):
        form = super(DataReqAdmin, self).get_form(request, obj, **kwargs)
        user = Group.objects.get(user=request.user)
        if user.name == 'pel_impor' or user.name == 'pel_lokal' or user.name == 'pel_intern':
            if getattr(obj, 'no_po', None) == 1 or getattr(obj, 'no_po', None) == None:
                form.base_fields['no_po'].queryset = form.base_fields['no_po'].queryset.filter(po_status=1)
        return form

    def queryset(self, request, obj=None):
        user = Group.objects.get(user=request.user)

        if request.user.is_superuser:
            return Data_Purchase_Request.objects.all()
        if user.name == 'kabag_proc':
            return Data_Purchase_Request.objects.filter(header_purchase_request_id__request_lock = True)
        elif user.name == 'pengendali_gudang' or user.name == 'pengendali_financial' or user.name == 'pengendali_proc':
            return Data_Purchase_Request.objects.all()
        elif user.name == 'kasi_lokal' or user.name == 'pel_lokal':
            return Data_Purchase_Request.objects.filter(header_purchase_request_id__request_lock = True, state_choices=1)
        elif user.name == 'kasi_impor' or user.name == 'pel_impor':
            return Data_Purchase_Request.objects.filter(header_purchase_request_id__request_lock = True, state_choices=2)
        elif user.name == 'kasi_intern' or user.name == 'pel_intern':
            return Data_Purchase_Request.objects.filter(header_purchase_request_id__request_lock = True, state_choices=3)

class HeaderRoAdmin(admin.ModelAdmin):
    list_display = ['no_reg','department','fiscal_year','ro_lock','total_expenditure','saldo','ro_type','ro_sent']
    search_fields = ['department__department']
    save_on_top = True
    ordering = ('-ro_month', )
    list_filter = ['ro_lock','department__department','fiscal_year__Code']
    inlines = [DataROInline,]

    def suit_row_attributes(self, obj, request):
        user = Group.objects.get(user=request.user)
        if user.name == 'pengendali_gudang':
            css_class = {
                False: 'error',
                }.get(obj.warehouse_agreement)
            if css_class:
                return {'class':css_class, 'data':obj.warehouse_agreement}
        elif user.name == 'pengendali_financial':
            css_class = {
                False: 'error',
                }.get(obj.financial_agreement)
            if css_class:
                return {'class':css_class, 'data':obj.financial_agreement}
        elif user.name == 'pengendali_proc':
            css_class = {
                False: 'error',
                }.get(obj.procurement_agreement)
            if css_class:
                return {'class':css_class, 'data':obj.procurement_agreement}
        else:
            css_class = {
                False: 'error',
                }.get(obj.ro_lock)
            if css_class:
                return {'class':css_class, 'data':obj.ro_lock}

    def get_form(self, request, obj=None, **kwargs):
        form = super(HeaderRoAdmin, self).get_form(request, obj, **kwargs)
        user = Group.objects.get(user=request.user)
        self.exclude = []
        if user.name == 'pengendali_gudang':
            self.exclude += ['financial_review','procurement_review',]
            if getattr(obj, 'request_lock', None) == True:
                self.exclude += ('warehouse_review',)
        elif user.name == 'pengendali_financial':
            self.exclude += ('warehouse_review','procurement_review',)
            if getattr(obj, 'request_lock', None) == True:
                self.exclude += ('financial_review',)
        elif user.name == 'pengendali_proc':
            self.exclude += ('warehouse_review','financial_review',)
            if getattr(obj, 'request_lock', None) == True:
                self.exclude += ('procurement_review',)
        else:
            self.exclude += ('warehouse_review','financial_review','procurement_review',)
        if getattr(obj, 'ro_sent', None) == False:
            self.exclude += ('warehouse_review','financial_review','procurement_review',)
        if request.user.is_superuser:
            self.exclude = []
        return form

    def get_readonly_fields(self, request, obj=None):
        data = Group.objects.get(user=request.user)
        readonly_fields = ()
        if data.name == 'pengendali_gudang':
            readonly_fields += ('f_rev','p_rev','financial_agreement','procurement_agreement','ro_sent','department','fiscal_year',)
            if getattr(obj, 'ro_lock', None) == True:
                readonly_fields += ('w_rev','warehouse_agreement',)
        elif data.name == 'pengendali_financial':
            readonly_fields += ('w_rev','p_rev','warehouse_agreement','procurement_agreement','ro_sent','department','fiscal_year',)
            if getattr(obj, 'ro_lock', None) == True:
                readonly_fields += ('f_rev','financial_agreement',)
        elif data.name == 'pengendali_proc':
            readonly_fields += ('w_rev','f_rev','warehouse_agreement','financial_agreement','ro_sent','department','fiscal_year',)
            if getattr(obj, 'ro_lock', None) == True:
                readonly_fields += ('p_rev','procurement_agreement',)
        elif data.name == 'asset':
            readonly_fields += ('w_rev','f_rev','p_rev','warehouse_agreement','financial_agreement',
                                'procurement_agreement',)
        else:
            readonly_fields += ('w_rev','f_rev','p_rev','warehouse_agreement','financial_agreement',
                                'procurement_agreement',)
        if getattr(obj, 'ro_sent', None) == False:
            readonly_fields += ('w_rev','f_rev','p_rev','warehouse_agreement','financial_agreement',
                                'procurement_agreement',)
        if getattr(obj, 'ro_sent', None) == True:
            readonly_fields += ('ro_sent','department','fiscal_year',)
        if request.user.is_superuser:
            readonly_fields = ()
        else:
            readonly_fields += ('ro_month','ro_lock','ro_lock_date','ro_type',)
        return readonly_fields

    def queryset(self, request, obj=None):
        user = Group.objects.get(user=request.user)
        if user.name == 'asset':
            return Header_Rush_Order.objects.filter(ro_type = 2)
        else: return Header_Rush_Order.objects.all()

class DataRoAdmin(admin.ModelAdmin):
    list_display = ['no_item', 'header_rush_order_id', 'ro_goods_name','ro_amount','currency_id','ro_unit_price',
                    'ro_total_rupiah','ro_total_price','method_choices','state_choices','no_po']
    search_fields = ['header_rush_order__id','ro_goods_name']
    save_on_top = True
    list_filter = ['header_rush_order_id__no_reg',]
    def get_form(self, request, obj=None, **kwargs):
        form = super(DataRoAdmin, self).get_form(request, obj, **kwargs)
        user = Group.objects.get(user=request.user)
        get = False
        try:
            gett = getattr(obj, 'header_rush_order_id', None)
            get = gett.ro_lock
        except:
            pass
        if get == False:
            if user.name == 'asset':
                if getattr(obj, 'header_rush_order_id', None) == None:
                    form.base_fields['header_rush_order_id'].queryset = form.base_fields['header_rush_order_id'].queryset.filter(ro_sent=False, ro_type=2)
        return form
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ()
        data = Group.objects.get(user=request.user)
        if data.name == 'asset':
            readonly_fields = ()
        else: readonly_fields = ('id', 'header_rush_order_id', 'ro_goods_name','goods_type_id','unit_of_measure_id', 'ro_used',
                                 'ro_amount','currency_id','ro_total_rupiah','ro_total_price','ro_detail',)
        get = False
        try:
            gett = getattr(obj, 'header_rush_order_id', None)
            get = gett.ro_lock
        except:
            pass
        if get == True:
            if data.name == 'kabag_proc':
                readonly_fields += ('method_choices','no_po','ro_unit_price',)
            elif data.name == 'kasi_impor' or data.name == 'kasi_lokal' or data.name == 'kasi_intern':
                readonly_fields += ('state_choices','no_po','ro_unit_price',)
            elif data.name == 'pel_impor' or data.name == 'pel_lokal' or data.name == 'pel_intern':
                readonly_fields += ('state_choices','method_choices',)
            elif data.name == 'pengendali_gudang' or data.name == 'pengendali_financial' or data.name == 'pengendali_proc':
                readonly_fields += ('state_choices','method_choices','no_po','ro_unit_price',)
            elif data.name == 'asset':
                readonly_fields += ('ro_goods_name','goods_type_id','unit_of_measure_id', 'ro_used','ro_amount','currency_id','ro_unit_price',
                                    'ro_total_rupiah','ro_total_price','ro_detail','state_choices','method_choices','no_po','header_rush_order_id',)
        else:
            xx = False
            try:
                x = getattr(obj, 'header_rush_order_id', None)
                xx = x.ro_sent
            except:
                pass
            if xx == True:
                if data.name == 'asset':
                    readonly_fields += ('ro_goods_name','goods_type_id','unit_of_measure_id', 'ro_used','ro_amount','currency_id','ro_unit_price',
                                        'ro_total_rupiah','ro_total_price','ro_detail','state_choices','method_choices','no_po','header_rush_order_id',)
            if data.name == 'asset':
                readonly_fields += ('state_choices','method_choices','no_po',)
            else: readonly_fields += ('state_choices','method_choices','no_po','ro_unit_price')
        if request.user.is_superuser:
            readonly_fields = ()
        return readonly_fields

    def queryset(self, request, obj=None):
        user = Group.objects.get(user=request.user)
        if user.name == 'kabag_proc':
            return Data_Rush_Order.objects.filter(header_rush_order_id__ro_lock = True)
        elif user.name == 'pengendali_gudang' or user.name == 'pengendali_financial' or user.name == 'pengendali_proc':
            return Data_Rush_Order.objects.all()
        elif user.name == 'kasi_lokal' or user.name == 'pel_lokal':
            return Data_Rush_Order.objects.filter(header_rush_order_id__ro_lock = True, state_choices=1)
        elif user.name == 'kasi_impor' or user.name == 'pel_impor':
            return Data_Rush_Order.objects.filter(header_rush_order_id__ro_lock = True, state_choices=2)
        elif user.name == 'kasi_intern' or user.name == 'pel_intern':
            return Data_Rush_Order.objects.filter(header_rush_order_id__ro_lock = True, state_choices=3)
        if user.name == 'asset':
            return Data_Rush_Order.objects.filter(header_rush_order_id__ro_type = 2)
        if request.user.is_superuser:
            return Data_Rush_Order.objects.all()

class BudgetAdmin(admin.ModelAdmin):
    list_display = ['budget_no','year','department','budget_value','budget_devided','hasil_bagi']
    def get_readonly_fields(self, request, obj=None):
        user = Group.objects.get(user=request.user)
        if user.name == 'pengendali_gudang' or user.name == 'pengendali_financial' or user.name == 'pengendali_proc':
            readonly_fields = ('budget_no','year','department','budget_value','budget_devided','hasil_bagi',)
        if request.user.is_superuser:
            readonly_fields = ()
        return readonly_fields

class PoAdmin(admin.ModelAdmin):
    list_display = ['no_reg','vendor','po_month','po_add_date','po_status','po_date_sent','total_','ppn10','total_expenditure', 'print_pdf',]
    search_fields = ['id', 'vendor__vendor_name','po_month']
    readonly_fields = ('po_date_sent',)
    list_filter = ['vendor__vendor_name',]
    inlines = [DataPPInline,DataROInline]

    def get_form(self, request, obj=None, **kwargs):
        form = super(PoAdmin, self).get_form(request, obj, **kwargs)
        user = Group.objects.get(user=request.user)
        self.exclude = []
        if user.name == 'pel_impor' or user.name == 'pel_lokal' or user.name == 'pel_intern':
            if getattr(obj, 'po_status', None) == 21 or getattr(obj, 'po_status', None) == 22:
                self.exclude += ['ship_to','po_agreement',]
            if getattr(obj, 'po_status', None) == 23:
                self.exclude += ['ship_to','po_agreement',]
        else: self.exclude += ['ship_to','po_agreement',]
        if request.user.is_superuser:
            self.exclude = []
        return form

    def get_readonly_fields(self, request, obj=None):
        user = Group.objects.get(user=request.user)
        readonly_fields = ()
        if user.name == 'pel_impor' or user.name == 'pel_lokal' or user.name == 'pel_intern':
            if getattr(obj, 'po_status', None) == 21 or getattr(obj, 'po_status', None) == 22:
                readonly_fields += ('vendor','delay_fine','set_of_delay','po_agreementx','goods_receipt_plan','ship_tox',)
            if getattr(obj, 'po_status', None) == 23:
                readonly_fields += ('vendor','delay_fine','set_of_delay','po_agreementx','goods_receipt_plan','po_status','ship_tox',)
        else:
            readonly_fields += ('vendor','ship_tox','delay_fine','set_of_delay','po_agreementx','goods_receipt_plan','po_status')
        if request.user.is_superuser:
            readonly_fields = ()
        return readonly_fields

class ProcAdmin(admin.ModelAdmin):
    list_display = ['title', 'proc_budget','proc_add_date','end_enlisting','end_bid','end_expostulating','status','winner_m','published']
    list_filter = ['published', 'proc_add_date']
    search_fields = ['title', 'detail_proc', 'proc_add_date']
    date_hierarchy = 'proc_add_date'
    save_on_top = True
    #prepopulated_fields = {"slug": ("title",)}
    inlines = [DataPPInline,DataROInline]
    inlines = [VendorProcInline,]

    def get_form(self, request, obj=None, **kwargs):
        form = super(ProcAdmin, self).get_form(request, obj, **kwargs)
        user = Group.objects.get(user=request.user)
        self.exclude = []
        if user.name == 'pel_impor':
            form.base_fields['data_purchase_request'].queryset = form.base_fields['data_purchase_request'].queryset.filter(header_purchase_request_id__request_lock=True, method_choices=1, state_choices=2)
            form.base_fields['data_rush_order'].queryset = form.base_fields['data_rush_order'].queryset.filter(header_rush_order_id__ro_lock=True, method_choices=1, state_choices=2)
        elif user.name == 'pel_lokal':
            form.base_fields['data_purchase_request'].queryset = form.base_fields['data_purchase_request'].queryset.filter(header_purchase_request_id__request_lock=True, method_choices=1, state_choices=1)
            form.base_fields['data_rush_order'].queryset = form.base_fields['data_rush_order'].queryset.filter(header_rush_order_id__ro_lock=True, method_choices=1, state_choices=1)
        elif user.name == 'pel_intern':
            form.base_fields['data_purchase_request'].queryset = form.base_fields['data_purchase_request'].queryset.filter(header_purchase_request_id__request_lock=True, method_choices=1, state_choices=3)
            form.base_fields['data_rush_order'].queryset = form.base_fields['data_rush_order'].queryset.filter(header_rush_order_id__ro_lock=True, method_choices=1, state_choices=3)
        else:
            self.exclude = ['detail_proc',]
        if request.user.is_superuser:
            self.exclude = []
        return form

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ()
        user = Group.objects.get(user=request.user)
        if user.name == 'pel_impor' or user.name == 'pel_lokal' or user.name == 'pel_intern':
            readonly_fields = ()
        else:
            readonly_fields += ('title','slug','winner_determination','classification','fields','sub_fields','detail_procx','winner','proc_budget','proc_add_date',
                                'data_purchase_request','data_rush_order','end_enlisting','end_bid','end_expostulating','status','winner_m','published','proc_doc',)
        if request.user.is_superuser:
            readonly_fields = ()
        return readonly_fields

class VendorProcAdmin(admin.ModelAdmin):
    list_display = ['id','ms_vendor','announcement_proc','bid_value','doc_bid']
    search_fields = ['id', 'ms_vendor__vendor_name','announcement_proc__title']
    inlines = [BiddingProcInline,]

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ()
        user = Group.objects.get(user=request.user)
        if request.user.is_superuser:
            readonly_fields = ()
        else:
            readonly_fields += ('ms_vendor','announcement_proc','bid_value','doc_bid',)
        return readonly_fields

class BiddingProcAdmin(admin.ModelAdmin):
    list_display = ['id','vendor_proc','msg_add_date','uname','msg']
    search_fields = ['id', 'vendor_proc__id']
    #readonly_fields = ('id','read_status','uname','msg_add_date',)

    def get_form(self, request, obj=None, **kwargs):
        form = super(BiddingProcAdmin, self).get_form(request, obj, **kwargs)
        user = Group.objects.get(user=request.user)
        self.exclude = []
        if user.name == 'pel_impor' or user.name == 'pel_lokal' or user.name == 'pel_intern':
            if getattr(obj, 'uname', None) == 'admin' or getattr(obj, 'uname', None) == None:
                self.exclude = []
            else:
                self.exclude += ['message',]
        else:
            self.exclude = ['message',]
        return form
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ()
        user = Group.objects.get(user=request.user)
        if user.name == 'pel_impor' or user.name == 'pel_lokal' or user.name == 'pel_intern':
            if getattr(obj, 'uname', None) == 'admin' or getattr(obj, 'uname', None) == None:
                readonly_fields = ('uname',)
            else:
                readonly_fields += ('vendor_proc','msg_add_date','uname','msg',)
        else:
            readonly_fields += ('vendor_proc','msg_add_date','uname','msg',)
        if request.user.is_superuser:
            readonly_fields = ()
        return readonly_fields

class BiddingItemInline(admin.TabularInline):
    model = Bidding_Request_Item
    extra = 0
    max_num = 0
    can_delete = True

class BiddingReqItemAdmin(admin.ModelAdmin):
    list_display = ['id','bidding_request','data_purchase_request','data_rush_order']
    search_fields = ['id', 'bidding_request__no_reg','data_purchase_request__no_reg','data_rush_order__no_reg']

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ()
        data = {}
        try:
            data = Bidding_Request.objects.get(id=getattr(obj, 'bidding_request__id', None))
            if data.br_status == 2:
                readonly_fields += ('bidding_request','data_purchase_request',)
        except:
            pass
        user = Group.objects.get(user=request.user)
        if user.name == 'kabag_proc':
            readonly_fields += ('bidding_request','data_purchase_request',)
        if request.user.is_superuser:
            readonly_fields = ()
        return readonly_fields

    def get_form(self, request, obj=None, **kwargs):
        form = super(BiddingReqItemAdmin, self).get_form(request, obj, **kwargs)
        user = Group.objects.get(user=request.user)
        if user.name == 'pel_lokal':
            form.base_fields['data_purchase_request'].queryset = form.base_fields['data_purchase_request'].queryset.filter(header_purchase_request_id__request_lock=True, method_choices=2, state_choices=1)
            form.base_fields['data_rush_order'].queryset = form.base_fields['data_rush_order'].queryset.filter(header_rush_order_id__ro_lock=True, method_choices=2, state_choices=1)
        elif user.name == 'pel_impor':
            form.base_fields['data_purchase_request'].queryset = form.base_fields['data_purchase_request'].queryset.filter(header_purchase_request_id__request_lock=True, method_choices=2, state_choices=2)
            form.base_fields['data_rush_order'].queryset = form.base_fields['data_rush_order'].queryset.filter(header_rush_order_id__ro_lock=True, method_choices=2, state_choices=2)
        elif user.name == 'pel_intern':
            form.base_fields['data_purchase_request'].queryset = form.base_fields['data_purchase_request'].queryset.filter(header_purchase_request_id__request_lock=True, method_choices=2, state_choices=3)
            form.base_fields['data_rush_order'].queryset = form.base_fields['data_rush_order'].queryset.filter(header_rush_order_id__ro_lock=True, method_choices=2, state_choices=3)
        if user.name == 'pel_lokal' or user.name == 'pel_impor' or user.name == 'pel_intern':
            form.base_fields['bidding_request'].queryset = form.base_fields['bidding_request'].queryset.filter(br_status = 1)
        return form

class BiddingReqAdmin(admin.ModelAdmin):
    list_display = ['no_reg','ms_vendor','br_add_date','br_end_date','br_status', 'bid_value', 'br_message','status','print_pdf',]
    search_fields = ['no_reg', 'vendor_proc__vendor_name']
    list_filter = ['br_status',]
    inlines = [BiddingItemInline,]

    def get_form(self, request, obj=None, **kwargs):
        form = super(BiddingReqAdmin, self).get_form(request, obj, **kwargs)
        user = Group.objects.get(user=request.user)
        self.exclude = []
        if request.user.is_superuser:
            self.exclude = []
        else:
            if getattr(obj, 'br_status', None) == 2:
                self.exclude += ['br_detail',]
        user = Group.objects.get(user=request.user)
        if user.name == 'kabag_proc':
            self.exclude += ['br_detail',]
        return form

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ()
        if request.user.is_superuser:
            readonly_fields = ()
        else:
            readonly_fields += ('br_sent_date','bid_value','br_message',)
            if getattr(obj, 'br_status', None) == 2:
                readonly_fields += ('ms_vendor','br_detailx','br_end_date','br_status',)
        user = Group.objects.get(user=request.user)
        if user.name == 'kabag_proc':
            readonly_fields += ('ms_vendor','br_detailx','br_end_date','br_status',)
        return readonly_fields

class RoleUserAdmin(admin.ModelAdmin):
    list_display = ['id','user','name']
    search_fields = ['user__username']

class GoodsTypeAdmin(admin.ModelAdmin):
    list_display = ['id','goods_type_detail']
    search_fields = ['goods_type_detail']

class UnitOMAdmin(admin.ModelAdmin):
    list_display = ['id','unit_of_measure_detail']
    search_fields = ['unit_of_measure_detail']

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['id','currency_symbol','currency_name','currency_rate']
    search_fields = ['currency_name']

class ClaimInline(admin.TabularInline):
    model = Claim
    extra = 0
    def get_readonly_fields(self, request, obj=None):
        data = Group.objects.get(user=request.user)
        readonly_fields = ()
        if data.name == 'kasi_impor' or data.name == 'kasi_lokal' or data.name == 'kasi_intern' or data.name == 'kabag_proc':
            readonly_fields = ('no_reg','goods_receipt_id','claim_add_date','claim_detail','claim_status','claim_sent_date',)
        if request.user.is_superuser:
            readonly_fields = ()
        return readonly_fields

class GoodsReceiptAdmin(admin.ModelAdmin):
    list_display = ['no_reg','purchase_order_id','delivery_orders','receipt_date','vendor_grade','denda','print_pdf']
    search_fields = ['no_reg','delivery_orders']
    inlines = [ClaimInline]

    def get_readonly_fields(self, request, obj=None):
        data = Group.objects.get(user=request.user)
        readonly_fields = ()
        if data.name == 'kasi_impor' or data.name == 'kasi_lokal' or data.name == 'kasi_intern' or data.name == 'kabag_proc':
            readonly_fields = ('no_reg','purchase_order_id','delivery_orders','receipt_date','vendor_grade',)
        if request.user.is_superuser:
            readonly_fields = ()
        return readonly_fields

class ClaimAdmin(admin.ModelAdmin):
    list_display = ['no_reg','goods_receipt_id','claim_add_date','claim_detail','claim_status','claim_sent_date']
    search_fields = ['no_reg','goods_receipt_id__no_reg']

    def get_readonly_fields(self, request, obj=None):
        data = Group.objects.get(user=request.user)
        readonly_fields = ()
        if data.name == 'kasi_impor' or data.name == 'kasi_lokal' or data.name == 'kasi_intern' or data.name == 'kabag_proc':
            readonly_fields = ('no_reg','goods_receipt_id','claim_add_date','claim_detail','claim_status','claim_sent_date',)
        else:
            if getattr(obj, 'claim_status', None) == 2:
                readonly_fields = ('no_reg','goods_receipt_id','claim_add_date','claim_detail','claim_status','claim_sent_date',)
        if request.user.is_superuser:
            readonly_fields = ()
        return readonly_fields

class ContractAdmin(admin.ModelAdmin):
    list_display = ['no_contract','vendor','no_po','con_add_date','start_date','end_date','status']
    search_fields = ['no_contract','vendor__vendor_name',]

    def suit_row_attributes(self, obj, request):
        css_class = {
            1: 'error', 2: 'success',
            }.get(obj.status_int())
        if css_class:
            return {'class':css_class, 'data':obj.status_int()}

    def get_readonly_fields(self, request, obj=None):
        data = Group.objects.get(user=request.user)
        readonly_fields = ()
        if data.name == 'kasi_impor' or data.name == 'kasi_lokal' or data.name == 'kasi_intern' or data.name == 'kabag_proc':
            readonly_fields = ('no_contract','vendor','no_po','con_add_date','start_date','end_date',)
        if request.user.is_superuser:
            readonly_fields = ()
        return readonly_fields

admin.site.register(Announcement_Proc, ProcAdmin)
admin.site.register(Vendor_Proc, VendorProcAdmin)
admin.site.register(Bidding_Proc, BiddingProcAdmin)
admin.site.register(Bidding_Request, BiddingReqAdmin)
admin.site.register(Bidding_Request_Item, BiddingReqItemAdmin)
admin.site.register(Ms_Vendor, MsVendorAdmin)
admin.site.register(Classification, ClassificationAdmin)
admin.site.register(Fields, FieldsAdmin)
admin.site.register(Sub_Fields, SubFieldsAdmin)
admin.site.register(Goods_Type, GoodsTypeAdmin)
admin.site.register(Unit_Of_Measure, UnitOMAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Set_Of_Delay, SetOfDelayAdmin)
admin.site.register(Budget, BudgetAdmin)

admin.site.register(User_Intern, UserInternAdmin)
admin.site.register(Header_Plan, HeaderPlanAdmin)
admin.site.register(Data_Plan, DataPlanAdmin)
admin.site.register(Header_Purchase_Request, HeaderReqAdmin)
admin.site.register(Data_Purchase_Request, DataReqAdmin)
admin.site.register(Header_Rush_Order, HeaderRoAdmin)
admin.site.register(Data_Rush_Order, DataRoAdmin)
admin.site.register(Purchase_Order, PoAdmin)
admin.site.register(Contract, ContractAdmin)
#admin.site.register(Group, RoleUserAdmin)

admin.site.register(Goods_Receipt, GoodsReceiptAdmin)
admin.site.register(Claim, ClaimAdmin)
