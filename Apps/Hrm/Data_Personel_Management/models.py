""" Develop By - Fery Febriyan Syah """

from django.db import models
from django.conf import settings
from Apps.Hrm.Master_Family.models import *
from Apps.Hrm.Master_General.models import *
from django.utils.translation import ugettext_lazy as _
from library.const.general import *
from library.const.group import GROUP
from library.const.province import PROVINCE
from PIL import Image
from datetime import datetime
from tinymce.models import HTMLField


class Employee(models.Model):
    employee = models.CharField (max_length=20, verbose_name="Nama Lengkap")
    birthday = models.DateField (verbose_name="Tanggal Lahir")
    religion = models.IntegerField (choices=RELIGION, verbose_name="Agama")
    gender = models.IntegerField (choices=GENDER, verbose_name="Jenis Kelamin")
    father_name = models.OneToOneField (Parent1, blank=True, null=True, verbose_name="Nama Ayah")
    mather_name = models.OneToOneField (Parent2, blank=True, null=True, verbose_name="Nama Ibu")
    wife_name = models.OneToOneField (Wife, blank=True, null=True, verbose_name="Nama Istri")
    child_name_1 = models.OneToOneField (Child1, blank=True, null=True, verbose_name="Nama Anak Pertama")
    child_name_2 = models.OneToOneField (Child2, blank=True, null=True,verbose_name="Nama Anak Kedua")
    national = models.IntegerField (choices=NATIONAL, verbose_name="Kewarganegaraan")
    province = models.IntegerField (choices=PROVINCE, verbose_name="Provinsi")
    city = models.CharField (max_length=50, verbose_name="Kota")
    address = HTMLField (max_length=50, verbose_name="Alamat", help_text=(' *)Alamat Lengkap'))
    house = models.IntegerField (verbose_name="Rumah", blank=True, null=True, choices=HOUSE,)
    status = models.IntegerField (choices=STATUS, verbose_name="Status", help_text=(' *)Status Perkawinan'))
    status_employee = models.IntegerField (choices=STATUS_EMPLOYEE, verbose_name="Status Pegawai")
    edu_status = models.IntegerField (choices=EDU_STATUS, verbose_name="Status Pendidikan", help_text=(' *)Pendidikan Terakhir'))
    nip = models.CharField (max_length=50, blank=False, verbose_name="NIP",)
    department = models.ForeignKey (Department, blank=False, verbose_name="Departemen")
    group = models.IntegerField (choices=GROUP, verbose_name="Golongan")
    section = models.ForeignKey (Section, verbose_name="seksi")
    npwp = models.CharField (max_length=50, blank=True, verbose_name="NPWP")
    weight = models.CharField (max_length=5, blank=True, verbose_name="Berat Badan", help_text=(' *)Contoh: 50 kg'))
    high = models.CharField (max_length=5, blank=True, verbose_name="Tinggi Badan", help_text=(' *)Contoh: 50 cm'))
    blood_group = models.IntegerField (choices=BLOOD, verbose_name="Golongan Darah")
    photo = models.ImageField (upload_to='uploads/employee/photo', blank=True, default='uploads/default.jpg', verbose_name="Foto Pegawai")
      
        
    class Meta:
        verbose_name = _('Pegawai')
        verbose_name_plural = _('Pegawai')
        ordering = ['id']
    
    def addressx(self):
        return '%s' % self.address
    addressx.allow_tags = True
    addressx.short_description = 'Alamat'
    
    def __unicode__(self):
        return '%s' % self.employee


    def display_image(self):
        return '<img src="%s%s" WIDTH="75" HEIGHT="75"/>' % (settings.MEDIA_URL, self.photo)
    
    display_image_description = 'Photo'
    display_image.allow_tags = True
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        if not self.photo:
            return

        photo = Image.open(self.photo)
        (width, height) = photo.size
        size = (110, 110)
        photo = photo.resize(size, Image.ANTIALIAS)
        photo.save(self.photo.path)
        super(Employee, self).save()
    
class Position (models.Model):
    employee = models.ForeignKey (Employee, verbose_name="Nama Pegawai")
    master_position = models.ForeignKey (Master_Position, verbose_name="Jabatan")
    department = models.ForeignKey (Department, verbose_name="Depatemen")
    level_position = models.ForeignKey (Level_Position, related_name=_('Tingkat Jabatan'), verbose_name="Tingkat Jabatan")
    date_decree = models.DateField (max_length=20, blank=True, null=True, verbose_name="Tanggal SK")
    number_decree = models.CharField (max_length=20, verbose_name="Nomer SK")
    group = models.IntegerField (choices=GROUP, verbose_name="Golongan")
    date_promotion = models.DateField (max_length=20, blank=True, null=True, verbose_name="Tanggal Promosi")
    unit_work = models.CharField (max_length=50, blank=True, null=True, verbose_name="Unit Kerja")
    
    
    class Meta:
        verbose_name = _('Jabatan')
        verbose_name_plural = _('Jabatan')
        ordering = ['id']
        
    def __unicode__(self):
        return '%s' % self.id
    
    
class Periodic_Increase_Decree (models.Model):
    employee = models.ForeignKey (Employee, verbose_name="Nama Pegawai")
    group = models.IntegerField (choices=GROUP, verbose_name="Golongan")
    number_periodic_increase_decree = models.CharField (max_length=50, editable=False, verbose_name="Nomer SK Berkala")
    working_life = models.CharField (max_length=50, blank=True, null=True, verbose_name="Masa Kerja", help_text=(' *)Contoh: 1 Tahun'))
    promotion_date = models.DateField (max_length=20, blank=True, null=True, verbose_name="Tanggal Promosi")
    expiration_date = models.DateField (max_length=20, blank=True, null=True, verbose_name="Masa Berlaku")
    delayed = models.DateField (max_length=20, blank=True, null=True, verbose_name="Ditunda")
    
    
    class Meta:
        verbose_name = _('SK Kenaikan Berkala')
        verbose_name_plural = _('SK Kenaikan Berkala')
        ordering = ['id']
        
    def incstring(self):
        try:
            data = Periodic_Increase_Decree.objects.all()
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
    
    def number_periodic_increase_decreee(self):
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
        return 'SKB/%(year)s/%(month)s/%(unik)s' % {'year': intyear, 'month': strnow, 'unik': number}
    
    def save(self, force_insert=True, force_update=True, using=None, update_fields=None):
        if self.number_periodic_increase_decree =='':
            self.number_periodic_increase_decree = self.number_periodic_increase_decreee()
        else:
            self.number_periodic_increase_decree = self.number_periodic_increase_decree
        super(Periodic_Increase_Decree, self).save()
        
    def __unicode__(self):
        return '%s' % self.number_periodic_increase_decree

    
class Group_Increase_Decree (models.Model):
    employee = models.ForeignKey (Employee, verbose_name="Nama Pegawai")
    group = models.IntegerField (choices=GROUP, verbose_name="Golongan")
    number_group_increase_decree = models.CharField (max_length=50, editable=False, verbose_name="Nomer SK")
    number_periodic_increase_decree = models.ForeignKey (Periodic_Increase_Decree, verbose_name="Nomer SK Golongan")
    working_life = models.CharField (max_length=50, blank=True, null=True, verbose_name="Masa Kerja", help_text=(' *)Contoh: 1 Tahun'))
    promotion_date = models.DateField (max_length=20, blank=True, null=True, verbose_name="Tanggal Promosi")
    expiration_date = models.DateField (max_length=20, blank=True, null=True, verbose_name="Masa Berlaku")
    delayed = models.DateField (max_length=20, blank=True, null=True, verbose_name="Ditunda")
    accelerated = models.DateField (max_length=20, blank=True, null=True, verbose_name="Dipercepat")
    
    
    class Meta:
        verbose_name = _('SK Kenaikan Golongan')
        verbose_name_plural = ('SK Kenaikan Golongan')
        ordering = ['id']
    
    def incstring(self):
        try:
            data = Group_Increase_Decree.objects.all()
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
    
    def number_group_increase_decreee(self):
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
        return 'SKG/%(year)s/%(month)s/%(unik)s' % {'year': intyear, 'month': strnow, 'unik': number}
    
    def save(self, force_insert=True, force_update=True, using=None, update_fields=None):
        if self.number_group_increase_decree =='':
            self.number_group_increase_decree = self.number_group_increase_decreee()
        else:
            self.number_group_increase_decree = self.number_group_increase_decree
        super(Group_Increase_Decree, self).save()
    
    def __unicode__(self):
        return '%s' % self.number_group_increase_decree


class Education (models.Model):
    employee = models.ForeignKey (Employee, verbose_name="Nama Pegawai")
    education_name = models.CharField (max_length=50, blank=True, null=True, verbose_name="Nama Pendidikan")
    institution = models.CharField (max_length=50, verbose_name="Institusi")
    major = models.CharField (max_length=50, verbose_name="Jurusan")
    predicate = models.CharField (max_length=20, verbose_name="IPK")
   
    class Meta:
        verbose_name = _('Riwayat Pendidikan')
        verbose_name_plural = _('Riwayat Pendidikan')
        ordering = ['id']
        
    def __unicode__(self):
        return '%s' % self.education_name
     
    
class Seminar (models.Model):
    employee = models.ForeignKey (Employee, verbose_name="Nama Pegawai")
    seminar_name = models.CharField (max_length=50, blank=True, null=True, verbose_name="Nama Seminar")
    seminar_genre = models.IntegerField (choices=SEMINAR, blank=True, null=True, verbose_name="Jenis Seminar")
    basic_knowledge = models.CharField (max_length=50, blank=True, null=True, verbose_name="Dasar Ilmu")
    city = models.CharField (max_length=50, blank=True, null=True, verbose_name="Kota")
    organized = models.CharField (max_length=50, blank=True, null=True, verbose_name="Penyelenggara")
    
    
    class Meta:
        verbose_name = _('Seminar')
        verbose_name_plural = _('Seminar')
        ordering = ['id']
        
    def __unicode__(self):
        return '%s' % self.seminar_name
    
    
class Appreciation (models.Model):
    employee = models.OneToOneField (Employee, verbose_name="Nama Pegawai")
    appreciation_name = models.CharField (max_length=50, blank=True, null=True, verbose_name="Nama Penghargaan")
    year = models.CharField (max_length=20, blank=True, null=True, verbose_name="Tahun Penghargaan")
    in_order_to = models.CharField (max_length=50, blank=True, null=True, verbose_name="Dalam Rangka")
    giver = models.CharField (max_length=50, blank=True, null=True, verbose_name="Pemberi")
    description = HTMLField (max_length=50, blank=True, verbose_name="Deskripsi")
    
    class Meta:
        verbose_name = _('Penghargaan')
        verbose_name_plural = _('Penghargaan')
        ordering = ['id']
        
    def __unicode__(self):
        return '%s' % self.appreciation_name
    

class Hobby (models.Model):
    employee = models.ForeignKey (Employee, verbose_name="Nama Pegawai")
    hobby_genre = models.IntegerField (choices=HOBBY, blank=True, null=True, verbose_name="Jenis Hobi")
    hobby_name = models.CharField (max_length=50, blank=True, null=True, verbose_name="Nama Hobi")
    achievement = models.CharField (max_length=50, blank=True, verbose_name="Prestasi")
    appreciation_name = models.ForeignKey (Appreciation, blank=True, null=True, verbose_name="Penghargaan")
    
    
    
    class Meta:
        verbose_name = _('Hobi')
        verbose_name_plural = _('Hobi')
        ordering = ['id']
        
    def __unicode__(self):
        return '%s' % self.hobby_name
    
        
class Task (models.Model):
    employee = models.ForeignKey (Employee, verbose_name="Nama Pegawai")
    task = models.IntegerField (choices=TASK, blank=True, null=True, verbose_name="Jenis Tugas")
    city = models.CharField (max_length=50, blank=True, null=True, verbose_name="Kota")
    Date = models.DateField (max_length=20, blank=True, null=True, verbose_name="Tanggal Tugas")
    in_order_to = models.CharField (max_length=50, blank=True, null=True, verbose_name="Dalam Rangka")
    description = HTMLField (max_length=50, blank=True, null=True, verbose_name="Deskripsi")
    
    
    class Meta:
        verbose_name = _('Tugas')
        verbose_name_plural = _('Tugas')
        ordering = ['id']
        
    def descriptionx(self):
        return '%s' % self.description
    descriptionx.allow_tags = True
    descriptionx.short_description = 'Deskripsi'    
        
    def __unicode__(self):
        return '%s' % self.task
    
    
class Leave (models.Model):
    employee = models.ForeignKey (Employee, verbose_name="Nama Pegawai")
    leave = models.IntegerField (choices=LEAVE, blank=True, null=True, verbose_name="Jenis Cuti")
    from_date = models.DateField (max_length=20, blank=True, null=True, verbose_name="Tanggal Mulai")
    end_date = models.DateField (max_length=20, blank=True, null=True, verbose_name="Tanggal Berakhir")
    status = models.IntegerField (choices=STATUS2, blank=True, null=True, verbose_name="Status")
    description = HTMLField (max_length = 50, blank=True, null=True, verbose_name="Deskripsi")
    
    
    class Meta:
        verbose_name = _('Cuti')
        verbose_name_plural = _('Cuti')
        ordering = ['id']
    
    def descriptionx(self):
        return '%s' % self.description
    descriptionx.allow_tags = True
    descriptionx.short_description = 'Deskripsi'
        
    def __unicode__(self):
        return '%s' % self.leave

    
class Sanction (models.Model):
    employee = models.ForeignKey (Employee, verbose_name="Nama Pegawai")
    sanction = models.IntegerField (choices=SANKSI, verbose_name="Nama Sangsi")
    from_date = models.DateField (max_length=20, verbose_name="Tanggal Mulai")
    end_date = models.DateField (max_length=20, verbose_name="Tanggal Berakhir")
    description = HTMLField (max_length=50, blank=True, verbose_name="Keterangan")
    
    class Meta:
        verbose_name = _('Sangsi')
        verbose_name_plural = _('Sangsi')
        ordering = ['id']
    
    def descriptionx(self):
        return '%s' % self.description
    descriptionx.allow_tags = True
    descriptionx.short_description = 'Deskripsi'
        
    def __unicode__(self):
        return '%s' % self.sanction
    
class Termination (models.Model):
    employee = models.ForeignKey (Employee, verbose_name="Nama Pegawai")
    termination = models.IntegerField (choices=TERMINATION, verbose_name="Nama Penghentian")
    motive = models.TextField (max_length=50, blank=True, verbose_name="Alasan")
    status = models.IntegerField (choices=STATUS2, verbose_name="Status")
    description = HTMLField (max_length=50, blank=True, verbose_name="Keterangan")
    
    class Meta:
        verbose_name = _('Penghentian')
        verbose_name_plural = _('Penghentian')
        ordering = ['id']
    
    def descriptionx(self):
        return '%s' % self.description
    descriptionx.allow_tags = True
    descriptionx.short_description = 'Deskripsi'
        
    def __unicode__(self):
        return '%s' % self.termination_name
    
         
class Mutation (models.Model):
    employee = models.ForeignKey (Employee, verbose_name="Nama Pegawai")
    group = models.IntegerField (choices=GROUP, verbose_name="Golongan")
    department_begin = models.ForeignKey (Department, related_name=_('Department Awal '), verbose_name="Departemen Awal")
    from_position = models.ForeignKey (Master_Position, related_name=_('Jabatan Awal '), verbose_name="Jabatan Awal")
    department_now = models.ForeignKey (Department, related_name=_('Department Sekarang '), verbose_name="Departemen Sekarang")
    from_position = models.ForeignKey (Master_Position, related_name=_('Jabatan Sekarang'), verbose_name="Jabatan Sekarang")
    from_date = models.DateTimeField (verbose_name="Terhitung dari")
    description = HTMLField (max_length=50, blank=True, verbose_name="Deskripsi")
    
    
    class Meta:
        verbose_name= _('Mutasi')
        verbose_name_plural= _('Mutasi')
        ordering = ['id']
    
    def descriptionx(self):
        return '%s' % self.description
    descriptionx.allow_tags = True
    descriptionx.short_description = 'Deskripsi'
        
    def __unicode__(self):
        return '%s' % self.id
   
    
    
