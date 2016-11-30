from django.contrib import admin

from tutorial.models import Tpost

# Register your models here.

class TpostAdmin(admin.ModelAdmin):
    list_display  = ('title', 'modify_date')
    list_filter   = ('modify_date',)

admin.site.register(Tpost, TpostAdmin)
