from django.contrib import admin
from .models import *

class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cargo') 
    search_fields = ('nombre',) 
    list_filter = ('cargo','active')

admin.site.register(Empleado, EmpleadoAdmin)

admin.site.register(Cargo)
admin.site.register(Venta)
admin.site.register(Recurso)
admin.site.register(CategoriaRecurso)
admin.site.register(Producto)
admin.site.register(CategoriaInventario)
admin.site.register(Categoria_Informe)
admin.site.register(Informe)
admin.site.register(Sucursal)

admin.site.register(RegistroEntrada)
admin.site.register(RegistroSalida)


