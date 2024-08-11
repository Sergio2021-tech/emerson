from django.shortcuts import render
from django.views import generic
from tienda.models import *
from django.contrib.auth import get_user_model
from django.views import View
from functools import reduce
from operator import or_
from django.db.models import Q
import operator
from django.urls import reverse

# Create your views here.
User = get_user_model()

class Home(generic.ListView):
    model = Productos
    template_name = 'base/index.html'
    context_object_name = 'productos'
    
    def get_queryset(self):
        queryset = Productos.objects.filter(estado='Activo')  # Filtrar por estado activo

        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(nombreProducto__icontains=query)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['productos_recientes'] = Productos.objects.filter(estado='Activo').order_by('-fecha_creacion')[:8]
        context['search_query'] = self.request.GET.get('q', '')
        return context
class Cart(generic.TemplateView):
    template_name = 'base/cart.html'

class Detail(generic.DetailView):
    model = Productos
    template_name = 'base/detail.html'
    context_object_name = "obj"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        producto = self.get_object()
        try:
            user = User.objects.get(username=producto.usuario_creacion)
            context['usuario_creacion_nombre_completo'] = f"{user.first_name} {user.last_name}"
        except User.DoesNotExist:
            context['usuario_creacion_nombre_completo'] = "Usuario no encontrado"
        context['producto_url'] = self.request.build_absolute_uri(reverse('detail', args=[producto.pk]))
        context['imagen_url'] = self.request.build_absolute_uri(producto.imagenProducto)

        return context
class Shop(View):
    template_name = 'base/shop.html'
    
    def get(self, request, *args, **kwargs):
        # Obtener las categorías seleccionadas y los rangos de precios seleccionados
        categorias_seleccionadas = request.GET.getlist('categorias')
        precios_seleccionados = request.GET.getlist('precio')
        query = request.GET.get('q')

        # Filtrar productos por estado activo
        productos = Productos.objects.filter(estado='Activo')

        # Filtrar por categorías seleccionadas
        if categorias_seleccionadas:
            productos = productos.filter(idCategoria__idCategoria__in=categorias_seleccionadas)

        # Filtrar por rangos de precios seleccionados
        price_filters = []
        for precio_range in precios_seleccionados:
            if precio_range == 'all':
                continue
            min_price, max_price = precio_range.split('-')
            price_filters.append(Q(precio__gte=min_price, precio__lt=max_price))
        
        if price_filters:
            productos = productos.filter(reduce(operator.or_, price_filters))

        # Filtrar por búsqueda
        if query:
            productos = productos.filter(nombreProducto__icontains=query)

        # Obtener los conteos de productos por cada rango de precio
        precio_counts = []
        for precio_range in precios_seleccionados:
            if precio_range == 'all':
                precio_counts.append({
                    'range': 'Todos los precios',
                    'count': productos.count()  # Conteo de todos los productos si se selecciona 'all'
                })
            else:
                min_price, max_price = precio_range.split('-')
                count = productos.filter(precio__gte=min_price, precio__lt=max_price).count()
                precio_counts.append({
                    'range': f'${min_price} - ${max_price}',
                    'count': count
                })

        categorias = Categoria.objects.all()
        
        context = {
            'productos': productos,
            'categorias': categorias,
            'categorias_seleccionadas': categorias_seleccionadas,
            'precios_seleccionados': precios_seleccionados,
            'precio_counts': precio_counts,
            'search_query': query,
        }
        return render(request, self.template_name, context)
class Checkout(generic.TemplateView):
    template_name = 'base/checkout.html'
    
class Contact(generic.TemplateView):
    template_name = 'base/contact.html'