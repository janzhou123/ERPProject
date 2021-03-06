from django.contrib import admin
from Apps.Manufacturing.MasterData.models import *
from Apps.Manufacturing.Manufacturing.models import *

class Master_MaterialAdmin(admin.ModelAdmin):
	list_display = ['Material_Name','Material_Type','material_reviewx','Material_Quantity','Unit_Measure',]
	list_filter = ['Material_Name',]
	search_filter = ['Material_Name',]
admin.site.register(Master_Material, Master_MaterialAdmin)

"""
class Master_BoMAdmin(admin.ModelAdmin):
	list_display = ['BoM','ManufacturingOrder','Add_Date',]
	list_filter = ['BoM',]
	search_filter = ['BoM',]
admin.site.register(Master_BoM, Master_BoMAdmin)

class Bill_Of_MaterialAdmin(admin.ModelAdmin):
	list_display = ['Master_BoM','Master_Material','Material_Quantity','Unit_Measure',]
	list_filter = ['Master_BoM',]
	search_filter = ['Master_BoM',]
admin.site.register(Bill_Of_Material, Bill_Of_MaterialAdmin)
"""

class rkap_productionAdmin(admin.ModelAdmin):		# rkap (rencana kapasitas & jadwal produksi)
	list_display = ['no_reg','speed_in','eff_in','order_in','weight_in','add_date_time',]
	list_filter = ['no_reg',]
	search_filter = ['no_reg',]
admin.site.register(rkap_production, rkap_productionAdmin)

class Unit_Of_MeasureAdmin(admin.ModelAdmin):
	list_display = ['Unit_of_Measure_Detail','UnitOfMeasure_reviewx',]
	list_filter = ['Unit_of_Measure_Detail',]
	search_filter = ['Unit_of_Measure_Detail',]
admin.site.register(Unit_Of_Measure, Unit_Of_MeasureAdmin)

class Production_MechineAdmin(admin.ModelAdmin):
	list_display = ['MC_Production','Current_Status','Acl_Production','Forklift_Quantity','BlowTorch_Quantity',]
	list_filter = ['MC_Production',]
	search_filter = ['MC_Production',]
admin.site.register(Production_Mechine, Production_MechineAdmin)
"""
class ACL_MechineAdmin(admin.ModelAdmin):
	list_display = ['Acl_Production','Current_Status',]
	list_filter = ['Acl_Production',]
	search_filter = ['Acl_Production',]
admin.site.register(ACL_Mechine, ACL_MechineAdmin)


class CartonAdmin(admin.ModelAdmin):
	list_display = ['Carton_Type','Carton_Quantity','Add_Time_Date',]
	list_filter = ['Carton_Type',]
	search_filter = ['Carton_Type',]
admin.site.register(Carton, CartonAdmin)
"""

class Master_TeamAdmin(admin.ModelAdmin):
	list_display = ['Team_Name','Initial_Team','descriptionx',]
	list_filter = ['Team_Name',]
	search_filter = ['Team_Name',]
admin.site.register(Master_Team, Master_TeamAdmin)


class ProductLabelAdmin(admin.ModelAdmin):
	list_display = ['no_reg','Product_Label','descriptionx','display_image',]
	list_filter = ['no_reg',]
	search_filter = ['no_reg',]
admin.site.register(ProductLabel, ProductLabelAdmin)

class ProductDesignAdmin(admin.ModelAdmin):
	list_display = ['no_reg','Product_Design','descriptionx','display_image',]
	list_filter = ['no_reg',]
	search_filter = ['no_reg',]
admin.site.register(ProductDesign, ProductDesignAdmin)

class Product_Dimension_DiameterAdmin(admin.ModelAdmin):
	list_display = ['no_reg','Diam_fd1','Diam_fd2','Diam_fd3','Diam_bd4','Diam_fd5','Diam_body_pinch','Diam_body_sh_s','descriptionx','Inspection_Products',]
	list_filter = ['no_reg',]
	search_filter = ['no_reg',]
admin.site.register(Product_Dimension_Diameter, Product_Dimension_DiameterAdmin)

class Product_Dimension_HeightAdmin(admin.ModelAdmin):
	list_display = ['no_reg','Height_h','Height_fh','Ovality_Body','Ovality_Finish_Ring','descriptionx','Inspection_Products',]
	list_filter = ['no_reg',]
	search_filter = ['no_reg',]
admin.site.register(Product_Dimension_Height, Product_Dimension_HeightAdmin)

class Product_VolumeAdmin(admin.ModelAdmin):
	list_display = ['no_reg','Bf_Capacity','Fill_Capacity','Fill_Point_From_Top','Weight','descriptionx','Inspection_Products',]
	list_filter = ['no_reg',]
	search_filter = ['no_reg',]
admin.site.register(Product_Volume, Product_VolumeAdmin)

class Product_PhysicsAdmin(admin.ModelAdmin):
	list_display = ['no_reg','Thermal_Shock','Wavy_Finish','Sunken_BP','Sloping_Finish','Internal_Pressure','Contact_Point','Bottom_PUp','Body_PDS','Bearing_Surface','Annealing_Cord','descriptionx','Inspection_Products',]
	list_filter = ['no_reg',]
	search_filter = ['no_reg',]
admin.site.register(Product_Physics, Product_PhysicsAdmin)
