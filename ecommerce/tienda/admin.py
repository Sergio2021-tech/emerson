from django.contrib import admin
from tienda.models import *
from django.utils import timezone

# Register your models here.


class ProductoImagenInline(admin.TabularInline):
    model = ProductoImagen
    extra = 1

@admin.register(Productos)
class ProductosAdmin(admin.ModelAdmin):
    list_display = ("idProducto", "nombreProducto", "precio", "usuario_creacion")
    inlines = [ProductoImagenInline]

    def save_model(self, request, obj, form, change):
        if not obj.usuario_creacion:
            obj.usuario_creacion = request.user.username
        obj.save()
        if not obj.fecha_creacion:
            obj.fecha_creacion = timezone.now()
        obj.save()

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(usuario_creacion=request.user.username)
        return queryset
admin.site.register(Categoria)