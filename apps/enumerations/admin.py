from django.contrib import admin
from models import Enumeration
from ajax_select import make_ajax_field
from ajax_select.fields import autoselect_fields_check_can_add
from ajax_select import make_ajax_form

from ajax_select.admin import AjaxSelectAdmin, AjaxSelectAdminTabularInline




class EnumerationAdmin(AjaxSelectAdmin):
    list_display = ('name', 'enumeration_type', 'number', 'status', )
    search_fields = ('number', 'status',)
    form = make_ajax_form(Enumeration, {'mailing_address': 'address',
                                        'location_address': 'address',
                                        'medical_record_storage_address': 'address',
                                        'ten_ninety_nine_address': 'address',
                                        'other_addresses': 'address',
                                        'correspondence_address':'address',
                                        'revalidation_address': 'address', 
                                        'managers': 'manager',
                                        'direct_addresses': 'direct',
                                        
                                        })
    
admin.site.register(Enumeration, EnumerationAdmin)


#class EnumerationInline(AjaxSelectAdminTabularInline):
#
#    # AjaxSelectAdminTabularInline enables the + add option
#
#    model = Enumeration
#    form = make_ajax_form(Enumeration, {
#                   'managers': 'manager',},
#                show_help_text=True)
#    extra = 2
#    
#    def get_formset(self, request, obj=None, **kwargs):
#        from ajax_select.fields import autoselect_fields_check_can_add
#        fs = super(EnumerationInline, self).get_formset(request, obj,**kwargs)
#        autoselect_fields_check_can_add(fs.form, self.model, request.user)
#        return fs
#    
#class EnumerationAdmin(AjaxSelectAdmin):
#    list_display = ('name', 'enumeration_type', 'number', 'status', )
#    search_fields = ('number', 'status',)
#
#
#
#    inlines = [
#        EnumerationInline,
#    ]
#
#admin.site.register(Enumeration, EnumerationAdmin)
#    