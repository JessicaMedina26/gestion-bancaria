from django.contrib import admin

from django.contrib.auth.models import Group
from .models import Departamento


class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ("nombre",)

    def has_delete_permission(self, request, obj=None):
        return False


# Register your models here.
admin.site.unregister(Group)
admin.site.register(Departamento, DepartamentoAdmin)
