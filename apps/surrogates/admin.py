from django.contrib import admin
from models import Surrogate, SurrogateRequest



class SurrogateAdmin(admin.ModelAdmin):
    search_fields = ('user', )
admin.site.register(Surrogate, SurrogateAdmin)

admin.site.register(SurrogateRequest)