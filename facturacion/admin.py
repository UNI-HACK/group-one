from django.contrib import admin
from facturacion import models

admin.site.register(models.Usuario)
admin.site.register(models.Categoria)
admin.site.register(models.Producto)
admin.site.register(models.Factura)
admin.site.register(models.DetalleFactura)
admin.site.register(models.DetalleCarro)
