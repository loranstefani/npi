from django.contrib import admin
from models import Surrogate, SurrogateRequest
from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin


class SurrogateAdmin(AjaxSelectAdmin):
    search_fields = ('user', )
    form = make_ajax_form(Surrogate, {'user': 'manager',
                                       'enumerations': 'enumeration', 
                                    })


admin.site.register(Surrogate, SurrogateAdmin)



class SurrogateRequestAdmin(AjaxSelectAdmin):
    search_fields = ('user', )
    list_display = ('user', 'enumeration', 'added')
    form = make_ajax_form(SurrogateRequest, {'user': 'manager',
                                       'enumeration': 'enumeration', 
                                    })


admin.site.register(SurrogateRequest, SurrogateRequestAdmin)