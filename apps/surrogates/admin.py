from django.contrib import admin
from models import Surrogate, SurrogateRequestEnumeration, SurrogateRequestEIN
from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin


class SurrogateAdmin(AjaxSelectAdmin):
    search_fields = ('user', )
    form = make_ajax_form(Surrogate, {'user': 'manager',
                                       'enumerations': 'enumeration', 
                                    })


admin.site.register(Surrogate, SurrogateAdmin)



class SurrogateRequestEnumerationAdmin(AjaxSelectAdmin):
    search_fields = ('user', )
    list_display = ('user', 'enumeration', 'added')
    form = make_ajax_form(SurrogateRequestEnumeration, {'user': 'manager',
                                       'enumeration': 'enumeration', 
                                    })


admin.site.register(SurrogateRequestEnumeration, SurrogateRequestEnumerationAdmin)




class SurrogateRequestEINAdmin(AjaxSelectAdmin):
    search_fields = ('user', 'ein')
    list_display = ('user', 'ein', 'added')
    form = make_ajax_form(SurrogateRequestEnumeration, {'user': 'manager',
                                    })


admin.site.register(SurrogateRequestEIN, SurrogateRequestEINAdmin)


