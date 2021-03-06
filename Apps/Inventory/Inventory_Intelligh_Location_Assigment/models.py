from django.db import models 
from django.utils.translation import ugettext as _
from Apps.Inventory.Inventory_Planing.models import Warehouse, Warehouse_material
from Apps.Inventory.Inventory_Handling.models import Ms_commodity, master_commodity
from Apps.Inventory.Property_Inv.models import type_commodity, quantity_commodity,  Jenis_satuan 

class Header_commodity (models.Model):
    name_warehouse = models.ForeignKey(Warehouse, verbose_name='Nama Gudang')
    date_now =  models.DateField (verbose_name="Hari", auto_now_add=True)
    lock = models.BooleanField (verbose_name='Kuci')
    
    class Meta:
        verbose_name_plural= _('Lock List Penyimpanan Barang Produksi')
        verbose_name= _('Lock List Penyimpanan Barang Produksi')
    
    def __unicode__(self):
        return u'%s' % self.id


class data_commodity (models.Model):
    header = models.ForeignKey (Header_commodity, verbose_name="Hari")
    name_commodity = models.ForeignKey (Ms_commodity, verbose_name= 'Nama Barang')
    type = models.ForeignKey (type_commodity, verbose_name='Jenis Barang')
    quantity = models.ForeignKey (quantity_commodity, verbose_name='Kualitas Barang')
    unit = models.ForeignKey (Jenis_satuan, verbose_name="Satuan Barang")
    saved_location = models.ForeignKey (Warehouse, verbose_name='Lokasi Penyimpanan')
    
    class Meta:
        verbose_name_plural= _('List Penyimpanan Barang Produksi')
        verbose_name= _('List Penyimpanan Barang Produksi')
        
        def __unicode__(self):
            return u'%s' % self.id


class Header_commodity_Material (models.Model):
    name_warehouse = models.ForeignKey(Warehouse_material, verbose_name='Nama Gudang')
    date_now =  models.DateField (verbose_name="Hari", auto_now_add=True)
    lock = models.BooleanField (verbose_name='Kuci')
    
    class Meta:
        verbose_name_plural= _('Lock List Penyimpanan Barang Material')
        verbose_name= _('Lock List Penyimpanan Barang Material')
    
    def __unicode__(self):
        return u'%s' % self.id


class data_commodity_Material (models.Model):
    header = models.ForeignKey (Header_commodity_Material, verbose_name="Hari")
    name_commodity = models.ForeignKey (master_commodity, verbose_name= 'Nama Barang')
    type = models.ForeignKey (type_commodity, verbose_name='Jenis Barang')
    quantity = models.ForeignKey (quantity_commodity, verbose_name='Kualitas Barang')
    unit = models.ForeignKey (Jenis_satuan, verbose_name="Satuan Barang")
    saved_location = models.ForeignKey (Warehouse_material, verbose_name='Lokasi Penyimpanan')
    
    class Meta:
        verbose_name_plural= _('List Penyimpanan Barang Material')
        verbose_name= _('List Penyimpanan Barang Material')
        
        def __unicode__(self):
            return u'%s' % self.id
        
