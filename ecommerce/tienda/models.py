from django.db import models
from django.core.validators import RegexValidator
from django.forms import ValidationError
from decimal import Decimal

repeatedLetters = RegexValidator(r'^(?!.*(\w)\1{2,}).+$', "No se pueden ingresar letras repetidas más de 2 veces")



        
class Categoria(models.Model):
    idCategoria = models.AutoField(primary_key=True,null=False,verbose_name='ID de Impuesto')
    nombreCategoria = models.CharField(max_length=50,verbose_name='Nombre')
    imagenCategoria = models.ImageField(null=True,blank=True,verbose_name='Imagen de Categoria')
    estado = models.CharField(max_length=50, editable=True, default="")

    def __str__(self):
        return str(self.nombreCategoria)

    def clean(self):
        nombreCategoria = self.nombreCategoria
        if '  ' in nombreCategoria:
            raise ValidationError('No se permiten doble espacios en el nombre de Categoria')
        return nombreCategoria
    
    @property
    def imageURL(self):
        try:
            url = self.imagenCategoria.url
        except: 
            url = ''
        return url
    class Meta: 
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

class Productos(models.Model):
    ESTADO_CHOICES = (
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    )
    idProducto = models.AutoField(primary_key=True,null=False,verbose_name='ID Producto')
    nombreProducto = models.CharField(max_length=100,unique = True,verbose_name='Nombre de Producto',validators=[repeatedLetters])
    descripcion = models.CharField(max_length=2000,verbose_name='Descripción',validators=[repeatedLetters])
    informacionAdicional = models.CharField(max_length=2000,verbose_name='Informacion Adicional',validators=[repeatedLetters])
    idCategoria = models.ForeignKey(Categoria,null=True,blank=True,on_delete=models.CASCADE,verbose_name='Categoria')
    precio = models.DecimalField(max_digits=10,decimal_places=2,blank=False,verbose_name='Precio')
    descuento = models.DecimalField(max_digits=10,null=True,decimal_places=2,verbose_name='Descuento')
    imagenProducto = models.ImageField(null=True,blank=True,verbose_name='Imagen principal del producto')
    usuario_creacion = models.CharField(max_length=50, editable=False, default="")
    fecha_creacion = models.DateTimeField(max_length=200,null=True,blank=True,editable=False,verbose_name='Fecha de Creacion',)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='Activo', verbose_name='Estado')
    contacto= models.CharField(max_length=10,verbose_name='Número telefónico')
    facebook = models.CharField(max_length=10,blank=True,null=True,verbose_name='Facebook')
   
    def __str__(self):
        return self.nombreProducto

    def clean(self):
        nombreProducto = self.nombreProducto
        descripcion = self.descripcion
        if '  ' in nombreProducto:
            raise ValidationError('No se permiten doble espacios en el nombre del Producto')
        elif '  ' in descripcion:
            raise ValidationError('No se permiten doble espacios en la descripción del Producto')
        return nombreProducto,descripcion


    def descuentoProducto(self):
        return self.precio * self.descuento
    
    def totalProductoDescuento(self):
        descuentoT = self.precio * self.descuento
        total_con_descuento = self.precio - descuentoT
        return total_con_descuento.quantize(Decimal('0.00'))

    @property
    def imageURL(self):
        try:
            url = self.imagenProducto.url
        except: 
            url = ''
        return url

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Productos"


class ProductoImagen(models.Model):
    producto = models.ForeignKey(Productos, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(verbose_name='Imagen del Producto')

    @property
    def imageURL(self):
        try:
            url = self.imagenProducto.url
        except: 
            url = ''
        return url