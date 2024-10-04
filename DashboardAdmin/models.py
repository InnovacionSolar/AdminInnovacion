from datetime import datetime
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.dispatch import receiver
import os

class Cargo(models.Model):
    nombre = models.CharField(max_length=500)

    def __str__(self):
        return self.nombre

class Empleado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    edad = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(18)], null=True, blank=True)
    correo = models.EmailField(max_length=254, blank=True, null=True)
    telefono = models.CharField(max_length=10)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_nac = models.DateField(null=True, blank=True)
    picture = models.ImageField(upload_to='usuarios/perfiles/', null=True, blank=True)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, null=True, blank=True)
    departamento = models.CharField(max_length=100, null=True, blank=True)
    DNI = models.CharField(max_length=8, null=True, blank=True)
    active = models.BooleanField(default=True)
    alias = models.CharField(max_length=100, null=True, blank=True)
    frase = models.CharField(max_length=100, null=True, blank=True)
    fondo = models.ImageField(upload_to='usuarios/fondos/', null=True, blank=True)
    
    def save(self, *args, **kwargs):
        try:
            this = Empleado.objects.get(id=self.id)
            if this.picture != self.picture and this.fondo != self.fondo:
                this.picture.delete(save=False)
                this.fondo.delete(save=False)
        except: pass 
        super().save(*args, **kwargs)

    def __str__(self):
        return '{} {}'.format(self.nombre, self.apellido)
    
@receiver(models.signals.post_delete, sender=Empleado)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.picture:
        if os.path.isfile(instance.picture.path):
            os.remove(instance.picture.path)
    
    

class Venta(models.Model):
    nombre = models.CharField(max_length=150)
    date_joined = models.DateField(default=datetime.now)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return str(self.nombre)
    

class CategoriaRecurso(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    
    def __str__(self):
        return str(self.nombre)
    
class Recurso(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    date_joined = models.DateField(auto_now_add=True)
    categoria = models.ForeignKey(CategoriaRecurso, on_delete=models.CASCADE)
    link = models.URLField(max_length=200, null=True, blank=True)
    documento = models.FileField(upload_to='documents/', null=True, blank=True)
    background = models.ImageField(upload_to='images/', null=True, blank=True)
    
    def __str__(self):
        return str(self.nombre)
    
    def save(self, *args, **kwargs):
        try:
            this = Recurso.objects.get(id=self.id)
            if this.documento != self.documento:
                this.documento.delete(save=False)
        except: pass 
        super().save(*args, **kwargs)
        
@receiver(models.signals.post_delete, sender=Recurso)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.documento:
        if os.path.isfile(instance.documento.path):
            os.remove(instance.documento.path)
            


class CategoriaInventario(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    
    def __str__(self):
        return str(self.nombre)   

class Sucursal(models.Model):
    nombre = models.CharField(max_length=150)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    
    def __str__(self):
        return str(self.nombre)
    
    def save(self, *args, **kwargs):
        try:
            this = Sucursal.objects.get(id=self.id)
            if this.logo != self.logo:
                this.logo.delete(save=False)
        except: pass 
        super().save(*args, **kwargs)
        

class Local(models.Model):
    ubicacion = models.CharField(max_length=150)
    nombre = models.CharField(max_length=150)
    telefono = models.CharField(max_length=10)
    empresa = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    encargado = models.ForeignKey(Empleado, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.nombre)
    
    
class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    date_joined = models.DateField(auto_now_add=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    picture = models.ImageField(upload_to='productos/', null=True, blank=True)
    categoria = models.ForeignKey(CategoriaInventario, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='productos')
    local = models.ForeignKey(Local, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.nombre)
    
    def save(self, *args, **kwargs):
        try:
            this = Producto.objects.get(id=self.id)
            if this.picture != self.picture:
                this.picture.delete(save=False)
        except: pass 
        super().save(*args, **kwargs)
        
@receiver(models.signals.post_delete, sender=Producto)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.picture:
        if os.path.isfile(instance.picture.path):
            os.remove(instance.picture.path)


class Categoria_Informe(models.Model):
    nombre = models.CharField(max_length=250)
    
    def __str__(self):
        return self.nombre
            
class Informe(models.Model):
    resumen = models.CharField(max_length=250)
    documento = models.FileField(upload_to='informes/', null=True, blank=True)
    categoria = models.ForeignKey(Categoria_Informe, on_delete=models.CASCADE)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.resumen
            
    def save(self, *args, **kwargs):
        try:
            this = Informe.objects.get(id=self.id)
            if this.documento != self.documento:
                this.documento.delete(save=False)
        except: pass 
        super().save(*args, **kwargs)
        
@receiver(models.signals.post_delete, sender=Informe)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.documento:
        if os.path.isfile(instance.documento.path):
            os.remove(instance.documento.path)
            
class RegistroEntrada(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    hora_ingreso = models.TimeField(auto_now_add=True)
    encargado = models.ForeignKey(Empleado, on_delete=models.CASCADE)

    def __str__(self):
        return f'Entrada de {self.producto.nombre} ({self.cantidad})'
    
class RegistroSalida(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    hora_salida = models.TimeField(auto_now_add=True)
    encargado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    motivo = models.TextField()
    ganacias = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'Salida de {self.producto.nombre} ({self.cantidad})'
    
class Notificacion(models.Model):
    mensaje = models.CharField(max_length=500, blank=True, null=True)
    imagen = models.ImageField(upload_to='notificaciones/', null=True, blank=True)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.mensaje