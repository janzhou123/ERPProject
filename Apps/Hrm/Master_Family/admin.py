''' @author: Fery Febriyan Syah '''


from django.contrib import admin
from Apps.Hrm.Master_Family.models import *



class WifeAdmin(admin.ModelAdmin):    
    list_display =('wife_name','birthday','religion','national','province','address','work','blood_group',)
    list_filter = ('wife_name',)
    list_search = ['wife_name',]
        
admin.site.register (Wife, WifeAdmin)

class Child1Admin(admin.ModelAdmin):
    list_display =('child_name_1','birthday','religion','gender','work','education_status','status','blood_group',)    
    list_filter = ('child_name_1','gender',)
    list_search = ['child_name_1','gender']
    
admin.site.register (Child1, Child1Admin) 

class Child2Admin (admin.ModelAdmin):
    list_display =('child_name_2','birthday','religion','gender','work','education_status','status','blood_group',)    
    list_filter = ('child_name_2','gender',)
    list_search = ['child_name_2','gender',]
    
admin.site.register (Child2, Child2Admin)
    
class Parent1Admin (admin.ModelAdmin):
    list_display =('father_name','birthday','national','province','address',)    
    list_filter = ('father_name',)
    list_search = ['father_name',]
    
admin.site.register (Parent1, Parent1Admin)
    
class Parent2Admin (admin.ModelAdmin):
    list_display =('mather_name','birthday','national','province','address',)    
    list_filter = ('mather_name',)
    list_search = ['mather_name',]
    
admin.site.register (Parent2, Parent2Admin)
