"""Develop By - Achmad Afiffudin N"""

from django.db import models
from django.utils.translation import ugettext as _
from django.db.models import signals
from datetime import datetime, timedelta
from decimal import Decimal
from Apps.Accounting.GeneralLedger.models import Ms_Account, Ms_Period, Ms_Journal, Ms_Fiscal_Years
from Apps.Hrm.Master_General.models import *
from Apps.Procurement.vendor.const.const import *
from Apps.Accounting.AccountReceivable.const import *
from Apps.Distribution.master_sales.models import *

class Ms_Currency(models.Model):
    Name = models.CharField(verbose_name=_('Nama '), max_length=25)
    Code = models.CharField(verbose_name=_('Kode '), unique=True, max_length=25)
    Rate = models.DecimalField(verbose_name=_('Kurs '), max_digits=12, decimal_places=2, blank=True)
    Pre_Symbol = models.CharField(verbose_name=_('Pre-Simbol '), blank=True, max_length=2)
    Post_Symbol = models.CharField(verbose_name=_('Post-Simbol '), blank=True, max_length=2)

    class Meta:
        verbose_name = _('Master Mata Uang')
        verbose_name_plural = _('Master Mata Uang')
        ordering = ['id']
        db_table = "FACB | Master Kurs"

    def __unicode__(self):
        return self.Name

class Ms_Tax(models.Model):
    Name = models.CharField(_('Nama '), max_length=25)
    Code = models.CharField(verbose_name=_('Kode '), unique=True, max_length=25)
    Description = models.TextField(verbose_name=_('Deskripsi '))
    Percentage = models.DecimalField(_('Persentase '), max_digits=4, decimal_places=1, default=0,
                                     help_text=_('*) Persentase pajak dalam angka'))

    class Meta:
        verbose_name = _('Master Pajak')
        verbose_name_plural = _('Master Pajak')
        ordering = ['id']
        db_table = "FACB | Master Tax"

    def __unicode__(self):
        return self.Name

class Ms_Bank(models.Model):
    Bank = models.ForeignKey(Bank, verbose_name=_('Nama Bank'), max_length=20)
    Bank_Account = models.BigIntegerField(_('No Rekening'), max_length=20)
    Bank_Branch = models.CharField(_('Bank Cabang'), max_length=20)
    Address = models.TextField(_('Alamat'))

    class Meta:
        verbose_name = _('Master Bank')
        verbose_name_plural = _('Master Bank')
        ordering = ('id',)
        db_table = "FACB | Master Bank"

    def __unicode__(self):
        return '%s ' % (self.Bank.name)

    def debit(self):
        total = Decimal(0)
        try:
            a = Tr_Bank.objects.filter(Bank__id=self.id)
            for b in a:
                total += b.Debit
        except:
            pass

        return total.quantize(Decimal('0.01'))

    def credit(self):
        total = Decimal(0)
        try:
            a = Tr_Bank.objects.filter(Bank__id=self.id)
            for b in a:
                total += b.Credit
        except:
            pass

        return total.quantize(Decimal('0.01'))

    def total(self):
        a = self.debit() - self.credit()
        return a
    total.short_description = _('Total')

class Ms_Cash(models.Model):
    Cash_No = models.CharField(_('Kode Kas'), unique=True, max_length=10)
    Cash_Name = models.CharField(_('Nama Kas'), max_length=20)
    Description = models.TextField(_('Deskripsi'),)

    class Meta:
        verbose_name = _('Master Kas')
        verbose_name_plural = _('Master Kas')
        ordering = ('Cash_No',)
        db_table = "FACB | Master Kas"

    def __unicode__(self):
        return '%s | %s' % (self.Cash_No, self.Cash_Name)

    def debit(self):
        total = Decimal(0)
        try:
            a = Tr_Cash.objects.filter(Cash__id=self.id)
            for b in a:
                total += b.Debit
        except:
            pass

        return total.quantize(Decimal('0.01'))

    def credit(self):
        total = Decimal(0)
        try:
            a = Tr_Cash.objects.filter(Cash__id=self.id)
            for b in a:
                total += b.Credit
        except:
            pass

        return total.quantize(Decimal('0.01'))

    def total(self):
        a = self.debit() - self.credit()
        return a
    total.short_description = _('Total')

class Bank(Ms_Bank):
    class Meta:
        proxy = True
        verbose_name = 'Pernyataan Bank '
        verbose_name_plural = 'Pernyataan Bank '

class Cash(Ms_Cash):
    class Meta:
        proxy = True
        verbose_name = 'Pernyataan Kas '
        verbose_name_plural = 'Pernyataan Kas '

class Tr_Bank(models.Model):
    Bank = models.ForeignKey(Ms_Bank, verbose_name=_('Bank '))
    Date = models.DateField(_('Tanggal Pembayaran'), default=datetime.now())
    Reference = models.CharField(_('Referensi'), max_length=20)
    Debit = models.DecimalField(verbose_name=_('Debit '), max_digits=20, decimal_places=2, default=0)
    Credit = models.DecimalField(verbose_name=_('Credit '), max_digits=20, decimal_places=2, default=0)

    class Meta:
        verbose_name = _('Transaksi Bank')
        verbose_name_plural = _('Transaksi Bank')
        ordering = ['-id']
        db_table = "FACB | Transaksi Bank"

    def __unicode__(self):
        return self.Reference

class Tr_Cash(models.Model):
    Cash = models.ForeignKey(Ms_Cash, verbose_name=_('Kas '))
    Date = models.DateField(_('Tanggal Pembayaran'), default=datetime.now())
    Reference = models.CharField(_('Referensi'), max_length=20)
    Debit = models.DecimalField(verbose_name=_('Debit '), max_digits=20, decimal_places=2, default=0)
    Credit = models.DecimalField(verbose_name=_('Credit '), max_digits=20, decimal_places=2, default=0)

    class Meta:
        verbose_name = _('Transaksi Cash')
        verbose_name_plural = _('Transaksi Cash')
        ordering = ['-id']
        db_table = "FACB | Transaksi Kas"

    def __unicode__(self):
        return self.Reference

class Budget(models.Model):
    budget_no = models.CharField(verbose_name='No Anggaran', max_length=30, editable=False)
    year = models.ForeignKey(Ms_Fiscal_Years, verbose_name='Tahun Fiscal')
    department = models.ForeignKey(Department, verbose_name='Departemen')
    budget_value = models.IntegerField(verbose_name='Nilai Budget')
    budget_devided = models.CharField(verbose_name='Dibagi', choices=DROP_DOWN_CHOICES, max_length=2)

    class Meta:
        verbose_name = 'Anggaran Belanja'
        verbose_name_plural = 'Anggaran Belanja'
        db_table = "FACB | Anggaran Belanja"

    def __unicode__(self):
        return '%s' % self.budget_no

    def hasil_bagi(self):
        n = float(self.budget_value) / float(self.budget_devided)
        return n

    def total(self):
        now = datetime.now()
        nowmonth = now.strftime('%m')
        nowyear = now.strftime('%Y')
        intnow = int(nowmonth)
        intyear = int(nowyear)

        if intnow == 12:
            intnow = 1
            intyear += 1
        else :
            intnow += 1

        periode = 0
        total_all1 = 0
        b_id = self.id
        b_value = self.budget_value
        b_devided = self.budget_devided

        strnow = str(intnow)
        if len(strnow) < 2 :
            strnow = '0%(strnow)s' % {'strnow' : strnow}
        bulan = '%(intyear)s%(strnow)s' % {'intyear':intyear,'strnow':strnow}
        bagi = int(b_value) / int(b_devided)
        bagian = 12 / int(b_devided)
        n = 1
        while n <= int(b_devided):
            temp = int(bagian) * n
            temp2 = (temp - int(bagian))+1
            if intnow <= temp and intnow > temp2:
                periode = n
                while temp2 <= temp:
                    strtemp2 = str(temp2)
                    strnow = strtemp2
                    if len(strtemp2) < 2 :
                        strnow = '0%(strtemp2)s' % {'strtemp2' : strtemp2}
                    else :
                        strnow = '%(strtemp2)s' % {'strtemp2' : strtemp2}
                    bln = '%(intyear)s%(strnow)s' % {'intyear':intyear,'strnow':strnow}
                    try:
                        hr = Header_Purchase_Request.objects.get(department=self.department,request_month=bln)
                        dr = Data_Purchase_Request.objects.filter(header_purchase_request_id=hr.id)
                        for drs in dr:
                            total_all1 += float(drs.request_total_price)
                    except:
                        pass
                    temp2 = temp2 + 1
            n = n + 1
        return total_all1

    def budget_id(self):
        year = self.year.Code
        departemen = self.department.department
        return '%(prefix)s | %(year)s | %(department)s' % {'prefix': 'ANGGARAN', 'year': year, 'department': departemen}

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.budget_no == "":
            self.budget_no = self.budget_id()
        else: self.budget_no = self.budget_no
        models.Model.save(self, force_insert, force_update, using, update_fields)

ADJUSTMENT_CHOICES =  getattr(settings, 'PAYMENT_STATUS_CHOICES', ((1, ugettext('Kas Ke Bank')),
                                                                   (2, ugettext('Bank Ke Kas'))))
class Tr_Adjustment_CashBank(models.Model):
    Adjustmen_No = models.CharField(verbose_name=_('No Pemindahan'), max_length=30, null=True, blank=True,
                                    help_text='*) Kosongkan form untuk mendapat Nomor otomatis')
    Type = models.IntegerField(_('Pemindahan '), choices=ADJUSTMENT_CHOICES)
    Cash = models.ForeignKey(Ms_Cash, verbose_name=_('Kas '))
    Bank = models.ForeignKey(Ms_Bank, verbose_name=_('Bank '))
    Date = models.DateField(_('Tanggal Pembayaran'), default=datetime.now())
    Journal = models.ForeignKey(Ms_Journal, verbose_name=_('Jurnal '), editable=False)
    Period = models.ForeignKey(Ms_Period, verbose_name=_('Periode '), editable=False)
    Value = models.DecimalField(verbose_name=_('Jumlah '), max_digits=20, decimal_places=2, default=0)
    Memo = models.TextField(verbose_name=_('Catatan '), null=True, blank=True, max_length=50)
    Control = models.BooleanField(verbose_name=_('Persetujuan'), default=False,
                                  help_text='*) Persetujuan Dilakukan Oleh Kadep Keuangan')

    class Meta:
        verbose_name = _('Pemindahan Kas/Bank')
        verbose_name_plural = _('Pemindahan Kas/Bank')
        ordering = ['-id']
        db_table = "FACB | Pemindahan Kas/Bank"

    def __unicode__(self):
        return self.Adjustmen_No

    def incstring(self):
        try:
            data = Tr_Adjustment_CashBank.objects.all().order_by('Date')
            jml = data.count()
        except:
            jml=0
            pass
        no = 0
        if jml == 0:
            no = 0
        else:
            for d in data:
                split = str(d.Adjustmen_No).split('/')
                no = int(split[4])
        num = no + 1
        cstring = str(num)
        return cstring

    def inclen(self):
        leng = len(self.incstring())
        return leng

    def adjustment_id(self):
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
        if self.Type == 1:
            return '%(kas)s/%(bank)s/%(year)s/%(month)s/%(unik)s' % {'kas': self.Cash.Cash_No, 'bank': self.Bank.Bank.name, 'year': intyear, 'month': strnow, 'unik': number}
        else:
            return '%(bank)s/%(kas)s/%(year)s/%(month)s/%(unik)s' % {'kas': self.Cash.Cash_No, 'bank': self.Bank.Bank.name, 'year': intyear, 'month': strnow, 'unik': number}

    def jurnal(self):
        a = Ms_Journal.objects.get(Type=8)
        return a

    def period(self):
        today = datetime.now().date()
        a = 0
        try:
            per = Ms_Period.objects.filter(Start_Period__lte=today, End_Period__gte=today)
            a = per.count()
        except:
            pass
        if a == 1:
            for x in per:
                b = x.Code
                c = Ms_Period.objects.get(Code=b)
        else:
            c = self.Period
        return c

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.Adjustmen_No == "":
            self.Adjustmen_No = self.adjustment_id()
        else:
            self.Adjustmen_No = self.Adjustmen_No
        self.Period = self.period()
        self.Journal = self.jurnal()
        super(Tr_Adjustment_CashBank, self).save()

def create_journal(sender, created, instance, **kwargs):
    from Apps.Accounting.GeneralLedger.models import Tr_Journal_Entry
    n=0
    a={}
    b={}
    try:
        a = Tr_Journal_Entry.objects.filter(Reference=instance.Adjustmen_No)
        n = a.count()
    except:
        pass
    if instance.Control==True:
        if n == 0:
            Tr_Journal_Entry.objects.create(Journal=instance.Journal, Journal_Period=instance.Period, Reference=instance.Adjustmen_No, Memo=instance.Memo)
        if instance.Type==1:
            n=0
            m=0
            try:
                a = Tr_Bank.objects.filter(Reference=instance.Adjustmen_No)
                n = a.count()
                b = Tr_Bank.objects.filter(Reference=instance.Adjustmen_No)
                m = b.count()
            except:
                pass
            if n == 0 and m == 0 :
                Tr_Cash.objects.create(Reference=instance.Adjustmen_No, Cash=instance.Cash, Debit=0, Credit=instance.Value)
                Tr_Bank.objects.create(Reference=instance.Adjustmen_No, Bank=instance.Bank, Debit=instance.Value, Credit=0)
        else:
            n=0
            m=0
            try:
                a = Tr_Bank.objects.filter(Reference=instance.Adjustmen_No)
                n = a.count()
                b = Tr_Bank.objects.filter(Reference=instance.Adjustmen_No)
                m = b.count()
            except:
                pass
            if n == 0 and m == 0 :
                Tr_Cash.objects.create(Reference=instance.Adjustmen_No, Cash=instance.Cash, Debit=instance.Value, Credit=0)
                Tr_Bank.objects.create(Reference=instance.Adjustmen_No, Bank=instance.Bank, Debit=0, Credit=instance.Value)
signals.post_save.connect(create_journal, sender=Tr_Adjustment_CashBank, weak=False, dispatch_uid='create_Journal')

def delete_journal(sender,instance, **kwargs):
    from Apps.Accounting.GeneralLedger.models import Tr_Journal_Entry, Detail_Journal_Entry
    Detail_Journal_Entry.objects.filter(Reference=instance.Adjustmen_No).delete()
    Tr_Journal_Entry.objects.filter(Reference=instance.Adjustmen_No).delete()
    Tr_Cash.objects.filter(Reference=instance.Adjustmen_No).delete()
    Tr_Bank.objects.filter(Reference=instance.Adjustmen_No).delete()
signals.post_delete.connect(delete_journal, sender=Tr_Adjustment_CashBank, weak=False, dispatch_uid='delete_Journal')

class Detail_Adjustment_Cash_Bank_Account(models.Model):
    Adjustment = models.ForeignKey(Tr_Adjustment_CashBank, verbose_name=_('Penyesuaian '))
    Account = models.ForeignKey(Ms_Account, verbose_name=_('Akun '))
    Type = models.IntegerField(_('Tipe Akun '), choices=ACCOUNT_VALUE)

    class Meta:
        verbose_name = _('Akun Penyesuaian Kas/Bank')
        verbose_name_plural = _('Akun Penyesuaian Kas/Bank')
        ordering = ['-id']
        db_table = "FACB | Akun Penyesuaian Kas/Bank"

    def __unicode__(self):
        return '%s' % self.Adjustment.Adjustment_No

def create_detail_Journal(sender, created, instance, **kwargs):
    from Apps.Accounting.GeneralLedger.models import Detail_Journal_Entry
    from Apps.Accounting.GeneralLedger.models import Tr_Journal_Entry
    if created:
        if instance.Type == 1:
            b=0
            try:
                je = Tr_Journal_Entry.objects.filter(Reference=instance.Adjustment.Adjustment_No)
                b = je.count()
            except:
                pass
            if b == 1:
                for j in je: Detail_Journal_Entry.objects.create(Reference=instance.Adjustment.Adjustment_No, Account=instance.Account, Journal_Entry=j,  Debit=instance.Adjustment.Value, Credit=0)
            else:
                Detail_Journal_Entry.objects.create(Reference=instance.Adjustment.Adjustment_No, Account=instance.Account, Debit=instance.Adjustment.Value, Credit=0)
        else:
            b=0
            try:
                je = Tr_Journal_Entry.objects.filter(Reference=instance.Adjustment.Adjustment_No)
                b = je.count()
            except:
                pass
            if b == 1:
                for j in je: Detail_Journal_Entry.objects.create(Reference=instance.Adjustment.Adjustment_No, Account=instance.Account, Journal_Entry=j, Debit=0, Credit=instance.Adjustment.Value)
            else:
                Detail_Journal_Entry.objects.create(Reference=instance.Adjustment.Adjustment_No, Account=instance.Account, Debit=0, Credit=instance.Adjustment.Value)
signals.post_save.connect(create_detail_Journal, sender=Detail_Adjustment_Cash_Bank_Account, weak=False, dispatch_uid='create_detail_Journal')

class Tr_Capital_Budget(models.Model):
    Capital_Budget_No = models.CharField(verbose_name=_('No Modal '), max_length=30, null=True, blank=True,
                                         help_text='*) Kosongkan form untuk mendapat Nomor otomatis')
    Bank = models.ForeignKey(Ms_Bank, verbose_name=_('Bank '))
    Date = models.DateField(_('Tanggal'), default=datetime.now())
    Journal = models.ForeignKey(Ms_Journal, verbose_name=_('Jurnal '), editable=False)
    Period = models.ForeignKey(Ms_Period, verbose_name=_('Periode '), editable=False)
    Value = models.DecimalField(verbose_name=_('Jumlah '), max_digits=20, decimal_places=2, default=0)
    Memo = models.TextField(verbose_name=_('Catatan '), null=True, blank=True, max_length=50)
    Control = models.BooleanField(verbose_name=_('Persetujuan'), default=False,
                                  help_text='*) Persetujuan Dilakukan Oleh Kadep Keuangan')

    class Meta:
        verbose_name = _('Modal')
        verbose_name_plural = _('Modal')
        ordering = ['-id']
        db_table = "FACB | Modal"

    def __unicode__(self):
        return self.Capital_Budget_No

    def incstring(self):
        try:
            data = Tr_Capital_Budget.objects.all().order_by('Date')
            jml = data.count()
        except:
            jml=0
            pass
        no = 0
        if jml == 0:
            no = 0
        else:
            for d in data:
                split = str(d.Capital_Budget_No).split('/')
                no = int(split[3])
        num = no + 1
        cstring = str(num)
        return cstring

    def inclen(self):
        leng = len(self.incstring())
        return leng

    def budget_id(self):
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
        return '%(prefik)s/%(bank)s/%(year)s/%(month)s/%(unik)s' % {'prefik': 'MODAL','bank': self.Bank.Bank.name, 'year': intyear, 'month': strnow, 'unik': number}

    def jurnal(self):
        a = Ms_Journal.objects.get(Type=9)
        return a

    def period(self):
        today = datetime.now().date()
        a = 0
        try:
            per = Ms_Period.objects.filter(Start_Period__lte=today, End_Period__gte=today)
            a = per.count()
        except:
            pass
        if a == 1:
            for x in per:
                b = x.Code
                c = Ms_Period.objects.get(Code=b)
        else:
            c = self.Period
        return c

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.Capital_Budget_No == "":
            self.Capital_Budget_No = self.budget_id()
        else:
            self.Capital_Budget_No = self.Capital_Budget_No
        self.Period = self.period()
        self.Journal = self.jurnal()
        super(Tr_Capital_Budget, self).save()

def create_journal(sender, created, instance, **kwargs):
    from Apps.Accounting.GeneralLedger.models import Tr_Journal_Entry
    n=0
    a={}
    try:
        a = Tr_Journal_Entry.objects.filter(Reference=instance.Capital_Budget_No)
        n = a.count()
    except:
        pass
    if instance.Control==True:
        if n == 0:
            Tr_Journal_Entry.objects.create(Journal=instance.Journal, Journal_Period=instance.Period, Reference=instance.Capital_Budget_No, Memo=instance.Memo)
            Tr_Bank.objects.create(Reference=instance.Capital_Budget_No, Bank=instance.Bank, Debit=instance.Value, Credit=0)
signals.post_save.connect(create_journal, sender=Tr_Capital_Budget, weak=False, dispatch_uid='create_Journal')

def delete_journal(sender,instance, **kwargs):
    from Apps.Accounting.GeneralLedger.models import Tr_Journal_Entry, Detail_Journal_Entry
    Detail_Journal_Entry.objects.filter(Reference=instance.Capital_Budget_No).delete()
    Tr_Journal_Entry.objects.filter(Reference=instance.Capital_Budget_No).delete()
    Tr_Bank.objects.filter(Reference=instance.Capital_Budget_No).delete()
signals.post_delete.connect(delete_journal, sender=Tr_Capital_Budget, weak=False, dispatch_uid='delete_Journal')

class Detail_Capital_Budget_Account(models.Model):
    Capital_Budget = models.ForeignKey(Tr_Capital_Budget, verbose_name=_('Modal '))
    Account = models.ForeignKey(Ms_Account, verbose_name=_('Akun '))
    Type = models.IntegerField(_('Tipe Akun '), choices=ACCOUNT_VALUE)

    class Meta:
        verbose_name = _('Akun Modal')
        verbose_name_plural = _('Akun Modal')
        ordering = ['-id']
        db_table = "FACB | Akun Modal"

    def __unicode__(self):
        return '%s' % self.Capital_Budget.Capital_Budget_No

def create_detail_Journal(sender, created, instance, **kwargs):
    from Apps.Accounting.GeneralLedger.models import Detail_Journal_Entry
    from Apps.Accounting.GeneralLedger.models import Tr_Journal_Entry
    if created:
        if instance.Type == 1:
            b=0
            try:
                je = Tr_Journal_Entry.objects.filter(Reference=instance.Capital_Budget.Capital_Budget_No)
                b = je.count()
            except:
                pass
            if b == 1:
                for j in je: Detail_Journal_Entry.objects.create(Reference=instance.Capital_Budget.Capital_Budget_No, Account=instance.Account, Journal_Entry=j,  Debit=instance.Capital_Budget.Value, Credit=0)
            else:
                Detail_Journal_Entry.objects.create(Reference=instance.Capital_Budget.Capital_Budget_No, Account=instance.Account, Debit=instance.Capital_Budget.Value, Credit=0)
        else:
            b=0
            try:
                je = Tr_Journal_Entry.objects.filter(Reference=instance.Capital_Budget.Capital_Budget_No)
                b = je.count()
            except:
                pass
            if b == 1:
                for j in je: Detail_Journal_Entry.objects.create(Reference=instance.Capital_Budget.Capital_Budget_No, Account=instance.Account, Journal_Entry=j, Debit=0, Credit=instance.Capital_Budget.Value)
            else:
                Detail_Journal_Entry.objects.create(Reference=instance.Capital_Budget.Capital_Budget_No, Account=instance.Account, Debit=0, Credit=instance.Capital_Budget.Value)
signals.post_save.connect(create_detail_Journal, sender=Detail_Capital_Budget_Account, weak=False, dispatch_uid='create_detail_Journal')
