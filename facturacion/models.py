from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    django_user = models.OneToOneField(User, on_delete=models.CASCADE)
    puntuacion = models.IntegerField(default=0)
    TIPOS = (
        ('Vendedor', 'Vendedor'),
        ('Comprador', 'Comprador'),
    )
    tipo = models.CharField(
        max_length=50,
        choices=TIPOS,
        default='Comprador',
    )

    def __str__(self):
        return self.django_user.username

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    en_descomposicion = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    precio = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    categoria = models.ForeignKey(Categoria)
    vendedor = models.ForeignKey(Usuario)
    activo = models.BooleanField(default=True)
    # foto

    def __str__(self):
        return self.nombre + ' - ' + str(self.vendedor)

    def agregar_descomposicion(self, q):
        self.cantidad = self.cantidad - q
        self.en_descomposicion = self.en_descomposicion + q
    
class Factura(models.Model):
    fecha_creacion = models.DateField(auto_now_add=True)
    requiere_envio = models.BooleanField()
    direccion_envio = models.CharField(max_length=1000)
    hora_envio = models.TimeField()
    anulado = models.BooleanField()
    entregado = models.BooleanField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    comentario = models.TextField(blank=True, null=True)
    po = models.CharField(max_length=100)
    comprador = models.ForeignKey(Usuario, related_name="fac_comprador")
    vendedor = models.ForeignKey(Usuario, related_name="fac_vendedor")

    def __str__(self):
        return self.po

    def anular(self):
        anulado = True

    def entregar(self):
        entregado = True

    def detalle(self):
        return DetalleFactura.objects.filter(factura=self.id)

class DetalleFactura(models.Model):
    factura = models.ForeignKey(Factura)
    producto = models.ForeignKey(Producto)
    anulado = models.BooleanField()
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.producto.nombre + ' - SubTotal $' + str(self.subtotal)

    def anular(self):
        anulado = True
        self.factura.total = self.factura.total - self.subtotal 