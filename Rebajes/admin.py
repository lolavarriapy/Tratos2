from django.contrib import admin
from .Models.mInformeTrabajo_estado import InformeTrabajo_estado
from .Models.mInformeTrabajo import InformeTrabajo
from .Models.mInformeTrabajo_detalle import InformeTrabajo_detalle


class InformeTrabajo_EstadoAdmin(admin.ModelAdmin):
    readonly_fields = ("fechaCreacion",)          

class InformeTrabajoAdmin(admin.ModelAdmin):
    readonly_fields = ("fechaCreacion",)        

class InformeTrabajoDetalleAdmin(admin.ModelAdmin):
    readonly_fields = ("fechaCreacion",)        

admin.site.register(InformeTrabajo_estado, InformeTrabajo_EstadoAdmin)
admin.site.register(InformeTrabajo, InformeTrabajoAdmin)
admin.site.register(InformeTrabajo_detalle, InformeTrabajoDetalleAdmin)

