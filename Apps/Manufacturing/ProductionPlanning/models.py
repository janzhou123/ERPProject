from django.db import models
from django.utils.translation import ugettext as _
from dateutil.relativedelta import relativedelta
from django.utils import timezone
#from apscheduler.scheduler import Scheduler
from datetime import *
from Apps.Manufacturing.const import *
#from Apps.Manufacturing.ProductionExecution.models import *
from Apps.Manufacturing.MasterData.models import Product_Dimension_Diameter, Product_Dimension_Height, ProductDesign, Product_Volume, Product_Physics, ProductLabel, Master_Material, Production_Mechine, rkap_production, Unit_Of_Measure
from Apps.Manufacturing.Manufacturing.models import Manufacturing_Order
from Apps.Distribution.order.models import OrderItem
from tinymce.models import HTMLField

class Master_Product (models.Model):          # <=> Specifation Product
    no_reg = models.CharField(verbose_name=_('Kode'), max_length=20, editable=False)
    Product_Name = models.CharField(verbose_name=_('Produk'), max_length=35, help_text='Isi Dengan Nama Produk')
    Description = HTMLField(verbose_name=_('Diskripsi'), blank=True, help_text='Penjelasan Singkat, Produk Digunakan Untuk Kemasan Tertentu')
    #HTMLField(verbose_name=_('Asset Staff Review '), blank=True) 'Desain Mold Botol'
    #Speed = models.IntegerField(_('Kecapatan'))
    #EML_Time = models.IntegerField(_('Waktu Perkiraan Paling Mungkin'))  #Estimated Most Likely Time
    #Pesseimistic_Time = models.IntegerField(_('Waktu Pesimis'))
    Dimension_Diameter = models.ForeignKey(Product_Dimension_Diameter, verbose_name=_('Diameter'))
    Dimension_Height = models.ForeignKey(Product_Dimension_Height, verbose_name=_('Tinggi'))
    Volume = models.ForeignKey(Product_Volume, verbose_name=_('Volume'))
    Physics = models.ForeignKey(Product_Physics, verbose_name=_('Fisik'))
    Product_Design = models.ForeignKey(ProductDesign, verbose_name=_('Design'))
    Product_Label = models.ForeignKey(ProductLabel, verbose_name=_('Label'))

    class Meta:
        verbose_name="Design Mould-Label"
        verbose_name_plural="1.Design Mould-Label"

    def products_reviewx(self):
        return '%s' % self.asset_staff_review
    products_reviewx.allow_tags = True
    products_reviewx.short_description = 'Desain Mold Botol'

    def incstring(self):
        try:
            data = Master_Product.objects.all()
            jml = data.count()
        except:
            jml=0
        pass
        no = 0
        if jml == 0:
            no = 0
        else:
            for d in data:
                split = str(d.no_reg).split('/')
                no = int(split[3])
        num = no + 1
        cstring = str(num)
        return cstring

    def inclen(self):
        leng = len(self.incstring())
        return leng

    def no_rek(self):
        date = datetime.now()
        now = date.strftime("%m")
        nowyear = date.strftime("%Y")
        intnow = int(now)
        intyear = int(nowyear)
        strnow = str(intnow)
        if len(strnow) < 2 :
            strnow = '0%(strnow)s' % {'strnow' : strnow}
        nol = 5 - self.inclen()
        if nol == 1: num = "0"
        elif nol == 2: num = "00"
        elif nol == 3: num = "000"
        elif nol == 4: num = "0000"
        number = num + self.incstring()
        return 'BTL/%(year)s/%(month)s/%(unik)s' % {'year': intyear, 'month': strnow, 'unik': number}

    def save(self, force_insert=True, force_update=True, using=None, update_fields=None):
        if self.no_reg =='':
            self.no_reg = self.no_rek()
        else:
            self.no_reg = self.no_reg
        super(Master_Product, self).save()
    def __unicode__(self):
        return u'%(no_reg)s--%(Product_Name)s' % {'no_reg':self.no_reg,'Product_Name':self.Product_Name}



class Bill_Of_Material (models.Model):
    #BoM_Id = models.IntegerField(verbose_name=_('Kode Komposisi'))
    Master_BoM = models.ForeignKey('Master_BoM', verbose_name=_('Master BoM'))
    Master_Material = models.ForeignKey(Master_Material, verbose_name=_('Material')) # ||===)> Isi Material=Item
    Material_Quantity = models.DecimalField(verbose_name=_('Jumlah'), max_digits=10, default=0.00, decimal_places=2)
    #DecimalField(verbose_name=_(''), max_digits=10, default=0.00, decimal_places=2)
    Unit_Measure = models.ForeignKey(Unit_Of_Measure, verbose_name=_('Satuan'))
    # Total_Quantity === nanti kasih Dev

    class Meta:
        verbose_name="Bahan BoM"
        verbose_name_plural="3.Bahan BoM"

    def materials(self):
        qm = self.Master_BoM.ManufacturingOrder.Product_Quantity * self.Material_Quantity
        return qm

    def __unicode__(self):
        return '%(id)s | %(Master_BoM)s' %{'id':self.id,'Master_BoM':self.Master_BoM}

class Master_BoM (models.Model):
    no_reg = models.CharField(verbose_name=_('Kode'), max_length=20, editable=False)
    ManufacturingOrder = models.ForeignKey(Manufacturing_Order, verbose_name='Manufacturing Order')
    Add_Date = models.DateField(verbose_name=_('Tanggal Pembuatan'), auto_now_add=True)

    class Meta:
        verbose_name="Master BoM"
        verbose_name_plural="2.Master BoM"

    def incstring(self):
        try:
            data = Master_BoM.objects.all()
            jml = data.count()
        except:
            jml=0
        pass
        no = 0
        if jml == 0:
            no = 0
        else:
            for d in data:
                split = str(d.no_reg).split('/')
                no = int(split[3])
        num = no + 1
        cstring = str(num)
        return cstring

    def inclen(self):
        leng = len(self.incstring())
        return leng

    def no_rek(self):
        date = datetime.now()
        now = date.strftime("%m")
        nowyear = date.strftime("%Y")
        intnow = int(now)
        intyear = int(nowyear)
        strnow = str(intnow)
        if len(strnow) < 2 :
            strnow = '0%(strnow)s' % {'strnow' : strnow}
        nol = 5 - self.inclen()
        if nol == 1: num = "0"
        elif nol == 2: num = "00"
        elif nol == 3: num = "000"
        elif nol == 4: num = "0000"
        number = num + self.incstring()
        return 'BoM/%(year)s/%(month)s/%(unik)s' % {'year': intyear, 'month': strnow, 'unik': number}

    def save(self, force_insert=True, force_update=True, using=None, update_fields=None):
        if self.no_reg =='':
            self.no_reg = self.no_rek()
        else:
            self.no_reg = self.no_reg
        super(Master_BoM, self).save()

    def __unicode__(self):
        return u'%s' % self.no_reg

"""
class Production_Mechine(models.Model):
	#Mechine_Id = models.
	MC_Production = models.CharField(verbose_name=_('M/C'), max_length=35, choices=Dapur) # G.1.=[1; 2; 3] D.G || G.2.=[1; 2; 3] D.G
	#M_C = models.CharField(verbose_name=_('M/C'),)
	Current_Status = models.IntegerField(verbose_name=_('Status'), choices=Status_Dapur) #PRODUKSI || STOP PRODUKSI


	class Meta:
		verbose_name="Mesin M/C"
		verbose_name_plural="2.Mesin M/C"

	def __unicode__(self):
		return u'%s' % self.MC_Production

class ACL_Mechine (models.Model):
	Acl_Production = models.CharField(verbose_name=_('ACL'), max_length=10, choices=ACL) # =ACL-[1; 2; 3; 4]
	Current_Status = models.IntegerField(verbose_name=_('Status'), choices=Status_ACL) #PRODUKSI || STOP PRODUKSI

	class Meta:
		verbose_name="Mesin ACL"
		verbose_name_plural="3.Mesin ACL"

	def __unicode__(self):
		return u'%s' % self.Acl_Production


class ACL_Mechine (models.Model):
	Acl_Production = models.IntegerField(verbose_name=_('ACL'), choices=ACL) # =ACL-[1; 2; 3; 4; 5; 6] # TIDAK DIPAKE

	class Meta:
		verbose_name="Mesin Label"
		verbose_name_plural="Mesin Label"

	def __unicode__(self):
		return '%s' % self.Acl_Production


class Carton(models.Model):
#	Carton_Id = models.CharField(verbose_name=_('Kode'), default='K', max_length=4)
	Carton_Type = models.CharField(verbose_name=_('Tipe'), max_length=25)
	Carton_Quantity = models.IntegerField(verbose_name=_('Jumlah'), default=0)
	Add_Time_Date = models.DateTimeField(verbose_name=_('Tanggal/Jam'), auto_now_add=True)

	class Meta:
		verbose_name="Karton"
		verbose_name_plural="Karton"
	def __unicode__(self):
		return self.Carton_Type

class Packing_Planning(models.Model):
#	Job_Num = models.IntegerField(verbose_name=_('Job'))
#	M_O = models.ForeignKey(Manufacturing_Order, verbose_name=_('Manufacturing Order'))
#	Start_Date = models.DateField(verbose_name=_('Mulai'))
#	End_Date = models.DateField(verbose_name=_('Selesai'))
	Carton = models.ForeignKey(Carton, verbose_name=_('Karton'))
	Plastic_Quantity = models.IntegerField(verbose_name=_('Plastik'), default=0)
	Line_Quantity = models.IntegerField(verbose_name=_('Tali'), default=0)
	Forklift_Quantity = models.IntegerField(verbose_name=_('Forklift'), default=0)
	BlowTorch_Quantity = models.IntegerField(verbose_name=_('Blow Torch'), default=0)
	Add_Time_Date = models.DateTimeField(verbose_name=_('Tanggal/Jam'), auto_now_add=True)

	class Meta:
		verbose_name="Rencana Packing"
		verbose_name_plural="Rencana Packing"
	def __unicode__(self):
		return u'%s' % self.Job_Num

class Master_Team(models.Model):
	Team_Name = models.CharField(verbose_name=_('Tim'), max_length=30, choices=TIM) # = Production || ACL
	Initial_Team = models.CharField(verbose_name=_('Regu'), max_length=5, choices=Initial) # =A, B, C, D, E, F, G, H
	Description_Material = models.TextField(verbose_name=_('Diskripsi'))
#	Material_Name = models.CharField(verbose_name=_('Nama'), max_length=15)
#	Material_Type = models.IntegerField(verbose_name=_('Tipe'), choices=Jenis_Material)
#	Material_Quantity = models.IntegerField(verbose_name=_('Jumlah')) #

	class Meta:
		verbose_name="Tim"
		verbose_name_plural="4.Tim"

	def __unicode__(self):
		return u'%s' % self.Initial_Team


class Master_Team (models.Model):
#	Team_Name = models.CharField(verbose_name=_('Tim Kerja'), max_length=15) # = Production || ACL
	Initial_Team = models.CharField(verbose_name=_('Inisial Regu'), max_length=15) # =A, B, C, D, E, F, G, H
#	Shift = models.CharField(verbose_name=_('Shift'), max_length=20) #Malam || Pagi

	class Meta:
		verbose_name="Tim Pelaksana"
		verbose_name_plural="Tim Pelaksana"

	def __unicode__(self):
		return '%s' % self.Team_Name



class rkap_production (models.Model):		# RAK PRODUCTION (rencana kapasitas & jadwal)
	rkap_id = models.CharField(verbose_name=_('Kode'), default='Rk', max_length=5)
	speed_in = models.DecimalField(verbose_name=_('Speed'), max_digits=5, default=0.00, decimal_places=2) #
	eff_in	= models.DecimalField(verbose_name=_('Efficiency'), max_digits=5, default=0.00, decimal_places=2) #
	order_in = models.IntegerField(verbose_name=_('Baik'), default=0) #rencana jumlah produk BAIK yang dihasilkan
	#broken_in = models.IntegerField(verbose_name=_('GAGAL'), default=0) #jumlah produk GAGAL yang dihasilkan
	weight_in = models.DecimalField(verbose_name=_('Berat'), max_digits=5, default=0.00, decimal_places=2) #berat produk hasil produksi
	add_date_time = models.DateTimeField(verbose_name=_('Tanggal/Jam')) #tanggal dibuat || waktu (07:00 - 07:00)=24 jam


	class Meta:
		verbose_name="RKA Produksi"
		verbose_name_plural="RKA Produksi"

	def __unicode__(self):
		return '%s' % self.rkap_id
"""
class production_plans (models.Model):
    no_reg = models.CharField(verbose_name=_('Job'), max_length=20, editable=False) #setiap eksekusi produk pada dapur memiliki no job yang beda
    M_O = models.ForeignKey(Manufacturing_Order, verbose_name='Manufacturing Order')
    Start_Date = models.DateTimeField(verbose_name=_('Mulai')) # DI HIDDEN
    End_Date = models.DateTimeField(verbose_name=_('Selesai')) # DI HIDDEN
    #	Long_Production = models.IntegerField(verbose_name=_('Lama'), default=0) # lama hari produksi ||
    #	MC_P = models.CharField(verbose_name=_('Mesin M/C'), max_length=25) # DI HIDDEN
    MC_P = models.ForeignKey(Production_Mechine, verbose_name=_('Mesin M/C')) # DI HIDDEN
    Product_Quantity_PerMC = models.IntegerField(verbose_name=_('Kapasitas M/C'), max_length=40) # DI HIDDEN
    #	ACL_M = models.ForeignKey(ACL_Mechine, verbose_name=_('Mesin Label'))
    Master_BoM = models.ForeignKey(Master_BoM, verbose_name=_('Master BoM'))
    #	Team_Work = models.ForeignKey(Master_Team, verbose_name=_('Tim')) # GAK USAH
    rka_production = models.ForeignKey(rkap_production, verbose_name=_('Target'), blank=True, null=True)
    plan_month = models.CharField(max_length=6, editable=False)


    class Meta:
        verbose_name="Production Schedule"
        verbose_name_plural="4.Production Schedule"

    def incstring(self):
        try:
            data = production_plans.objects.all()
            jml = data.count()
        except:
            jml=0
        pass
        no = 0
        if jml == 0:
            no = 0
        else:
            for d in data:
                split = str(d.no_reg).split('/')
                no = int(split[3])
        num = no + 1
        cstring = str(num)
        return cstring

    def inclen(self):
        leng = len(self.incstring())
        return leng

    def no_rek(self):
        date = datetime.now()
        now = date.strftime("%m")
        nowyear = date.strftime("%Y")
        intnow = int(now)
        intyear = int(nowyear)
        strnow = str(intnow)
        if len(strnow) < 2 :
            strnow = '0%(strnow)s' % {'strnow' : strnow}
        nol = 5 - self.inclen()
        if nol == 1: num = "0"
        elif nol == 2: num = "00"
        elif nol == 3: num = "000"
        elif nol == 4: num = "0000"
        number = num + self.incstring()
        return 'J/%(year)s/%(month)s/%(unik)s' % {'year': intyear, 'month': strnow, 'unik': number}

    def Durasi(self):
        d = self.End_Date - self.Start_Date
        return d

    def quantity_prod(self):
        detail = OrderItem.objects.get(so_reff__id=self.M_O.Production_Request.id)
        #Q = self.M_O.Production_Request.quantity + (self.M_O.Production_Request.quantity * 0.15)
        Q = detail.quantity + (detail.quantity * 0.15)
        return Q

    def start_p(self):
        n = 0
        now = timezone.now()
        start = end = now
        #try:
        end1 = end2 = end3 = {}
        d_end1 = d_end2 = d_end3 = now
        ada1 = ada2 = ada3 = 0
        try:
            end1 = production_plans.objects.filter(MC_P__MC_Production='G.1.1 D.G').order_by('-End_Date')[:1]
            ada1 = 1
            for e in end1:
                d_end1 = e.End_Date
        except:
            ada1 = 0
            pass
        try:
            end2 = production_plans.objects.filter(MC_P__MC_Production='G.1.2 D.G').order_by('-End_Date')[:1]
            ada2 = 1
            for e in end2:
                d_end2 = e.End_Date
        except:
            ada2 = 0
            pass
        try:
            end3 = production_plans.objects.filter(MC_P__MC_Production='G.1.3 D.G').order_by('-End_Date')[:1]
            ada3 = 1
            for e in end3:
                d_end3 = e.End_Date
        except:
            ada3 = 0
            pass
        if (ada1 == 1) and (ada2 == 1) and (ada3 == 1) :
            if (d_end1 <= d_end2) and (d_end1 <= d_end3):
                end = d_end1
            elif (d_end2 <= d_end1) and (d_end2 <= d_end3):
                end = d_end2
            else:
                end = d_end3
            start = end + relativedelta(days=1)
        else:
            start = start + relativedelta(days=1)
        #except:
        #	start = start + relativedelta(days=1)
        #	pass
        return start

    def end_p(self):
        end = datetime.now()
        duration = float(float(self.quantity_prod())/(float(self.rka_production.speed_in))) #
        mod = duration % 1440
        dur_min_mod = duration - mod

        n_day = dur_min_mod / 1440
        end = (self.start_p() + timedelta(n_day,mod))
        return end


    #	def xx(self):
    #		end = datetime.now()
    #		duration =float(float(self.quantity_prod())/(float(self.rka_production.speed_in))) #
    #		mod = duration % 1440
    #		dur_min_mod = duration - mod

    #		n_day = dur_min_mod / 1440
    #		return duration


    def machine(self):
        m = ''
        #try:
        now = timezone.now()
        end1 = end2 = end3 = {}
        ada1 = ada2 = ada3 = 0
        d_end1 = d_end2 = d_end3 = now
        try:
            end1 = production_plans.objects.filter(MC_P__MC_Production='G.1.1 D.G').order_by('-End_Date')[:1]
            ada1 = 1
            for e in end1:
                d_end1 = e.End_Date
        except:
            ada1 = 0
            pass
        try:
            end2 = production_plans.objects.filter(MC_P__MC_Production='G.1.2 D.G').order_by('-End_Date')[:1]
            ada2 = 1
            for e in end2:
                d_end2 = e.End_Date
        except:
            ada2 = 0
            pass
        try:
            end3 = production_plans.objects.filter(MC_P__MC_Production='G.1.3 D.G').order_by('-End_Date')[:1]
            ada3 = 1
            for e in end3:
                d_end3 = e.End_Date
        except:
            ada3 = 0
            pass
        if (ada1 == 1) and (ada2 == 1) and (ada3 == 1) :
            if (d_end1 <= d_end2) and (d_end1 <= d_end3):
                m = 'G.1.1 D.G'
            elif (d_end2 <= d_end1) and (d_end2 <= d_end3):
                m = 'G.1.2 D.G'
            else:
                m = 'G.1.3 D.G'
        elif ada1 == 1 and ada2 == 0:
            m = 'G.1.2 D.G'
        else: m = 'G.1.3 D.G'
        #except:
        #	m = 'G.1.1 D.G'
        #	pass
        return m

    def plan_mon(self):
        date = datetime.now()
        now = date.strftime("%m")
        nowyear = date.strftime("%Y")
        intnow = int(now)
        intyear = int(nowyear)
        strnow = str(intnow)

        if len(strnow) < 2 :
            strnow = '0%(strnow)s' % {'strnow' : strnow}

        return '%(year)s%(month)s' % {'year':intyear, 'month':strnow}

    def cetak(self):
        link = '<a href="/admin/manufacturing/reportmanufacturing/%(id)s" target="blank">Cetak</a>' % {'id':self.id}
        return link
    cetak.allow_tags = True
    cetak.short_descriptions=_('Print')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.no_reg =='':
            self.no_reg = self.no_rek()
        else:
            self.no_reg = self.no_reg
        self.Start_Date = self.start_p()
        self.End_Date = self.end_p()
        self.MC_P = Production_Mechine.objects.get(MC_Production = self.machine())
        self.Product_Quantity_PerMC = self.quantity_prod()
        if self.plan_month == '':
            self.plan_month = self.plan_mon()
        else: self.plan_month = self.plan_month
        super(production_plans, self).save()

    def __unicode__(self):
        return u'%s' % self.no_reg


"""
Program Evaluation and Review Technique (PERT)
______________________________________________

[ optimistic time + 4 X (Estimated Time Most Likely ) + pesseimistic] : 6


==>>

class nyoba_calender(models.Model):
	test = models.CharField(verbose_name=_('nyoba scheduler'), max_length=35)

	class Meta:
		verbose_name="nyoba scheduler"
		verbose_name_plural="nyoba scheduler"

	def __unicode__(self):
		return u'%s' % self.test

sched = Scheduler()
sched.start()

def job_funtion():
	print "Hello World"
	sched.add_cron_job(job_function, month='6-8,11-12', day='3rd fri', hour='0-3')


"""
#Create your models here.
