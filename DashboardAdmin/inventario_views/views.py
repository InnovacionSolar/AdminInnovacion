from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from ..models import Sucursal, Producto, Local, RegistroEntrada,RegistroSalida,Empleado
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from ..forms import CategoriaInventarioForm, ProductoForm, EmpresaForm, RegistroSalidaForm,RegistroEntradaForm
import os
from datetime import datetime


class InventarioHomeView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')
    permission_denied_message = "No tienes permisos para acceder a esta página."
 
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser or self.request.user.groups.filter(name='InventarioPermisos').exists() or self.request.user.groups.filter(name='VariosPermisos').exists()

    def handle_no_permission(self):
        return redirect('Home_User')
    
    def get(self,request, *args, **kwargs):
        empresas = Sucursal.objects.all() 
        try:
            empresa = get_object_or_404(Sucursal, id=kwargs.get('pk')) if 'pk' in kwargs else Sucursal.objects.first()
            empresaselect = empresa
            locales =Local.objects.filter(empresa=empresaselect)
        except:
            empresaselect = None
            empresa = Sucursal.objects.first()
            locales =Local.objects.filter(empresa=empresa)

        productos = Producto.objects.filter(sucursal=empresa).select_related('categoria', 'local')
        message = messages.get_messages(request)

        tiene_permisos_inventario = request.user.groups.filter(name='InventarioPermisos').exists() or self.request.user.groups.filter(name='VariosPermisos').exists()

        context = {
            'url':'Inventario',
            'productos': productos,
            'formcat' :  CategoriaInventarioForm(),
            'formprod' : ProductoForm(),
            'empresaform' : EmpresaForm(),
            'logsentrada': RegistroEntrada.objects.all(),
            'logssalida': RegistroSalida.objects.all(),
            'message': message,
            'empresas': empresas,
            'hora': datetime.now(),
            'empresaselect': empresaselect,
            'locales':locales,
            'tiene_permisos_inventario': tiene_permisos_inventario,
            'AZURE_SAS_TOKEN': os.environ.get('AZURE_SAS_TOKEN', ''),
        }
        return render(request,'Inventario/Home.html',context)
    
    def post(self,request, *args, **kwargs):
        if 'categoria_submit' in request.POST:
            form = CategoriaInventarioForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Categoria creada con éxito')
            else:
                messages.error(request, 'Error al crear la categoria')
                
        elif 'producto_submit' in request.POST:
            form = ProductoForm(request.POST, request.FILES)

            if form.is_valid():
                producto = form.save(commit=False)
    
                encargado = request.user.empleado if not request.user.is_superuser else None
                
                if encargado:
                    RegistroEntrada.objects.create(producto=producto, encargado=encargado, cantidad=request.POST.get('stock'))
                
                producto.stock = int(request.POST.get('stock'))
                producto.save()

                messages.success(request, 'Producto creado con éxito')
            else:
                messages.error(request, 'Error al crear el producto')
        elif 'empresa_submit' in request.POST:
            form = EmpresaForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Sucursal creada con éxito')
            else:
                messages.error(request, 'Error al crear la empresa')
        
        return redirect('Inventario_Home')
    
    
class InventarioDetailView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')
    permission_denied_message = "No tienes permisos para acceder a esta página."

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser or self.request.user.groups.filter(name='InventarioPermisos').exists() or self.request.user.groups.filter(name='VariosPermisos').exists()

    def handle_no_permission(self):
        return redirect('Home_User')
    
    def get(self,request, *args, **kwargs):
        product = Producto.objects.filter(id=kwargs['pk'])
        context = {
            'url':'Inventario',
            'products': product,
            'url':'Inventario'
        }
        return render(request,'Inventario/Detail.html',context)

class InventarioEditView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')
    permission_denied_message = "No tienes permisos para acceder a esta página."

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser or self.request.user.groups.filter(name='InventarioPermisos').exists() or self.request.user.groups.filter(name='VariosPermisos').exists()

    def handle_no_permission(self):
        return redirect('Home_User')
    
    def get(self,request, *args, **kwargs):
        Product = get_object_or_404(Producto, id=kwargs['pk'])
        ProductForm = ProductoForm(instance=Product)
        message = messages.get_messages(request)

        context = {
            'form': ProductForm,
            'message': message,
            'url':'Inventario'
        }
        return render(request,'Inventario/Edit.html', context)
    
    def post(self, request, *args, **kwargs):
        Product = get_object_or_404(Producto, id=kwargs['pk'])
        ProductForm = ProductoForm(request.POST, request.FILES, instance=Product)
        if ProductForm.is_valid():
            ProductForm.save()
            messages.success(request, 'Producto editado con éxito')
        else:
            messages.error(request, 'Error al editar el producto')
        return redirect('Inventario_Home')


class InventarioDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')
    permission_denied_message = "No tienes permisos para acceder a esta página."

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser or self.request.user.groups.filter(name='InventarioPermisos').exists() or self.request.user.groups.filter(name='VariosPermisos').exists()

    def handle_no_permission(self):
        return redirect('Home_User')
    
    def get(self,request, *args, **kwargs):
        Product = get_object_or_404(Producto, id=kwargs['pk'])
        message = messages.get_messages(request)

        context = {
            'product':Product,
            'message': message,

        }
        return render(request, 'Inventario/Delete.html',context)

    
    def post(self,request, *args, **kwargs):
        product = get_object_or_404(Producto, id=kwargs['pk'])
        try:
            product.delete()
            messages.success(request, 'Producto eliminado con éxito')
        except:
            messages.error(request, 'Error al eliminar el producto')
        return redirect('Inventario_Home')

class RegistrarSalidaViewHome(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')
    permission_denied_message = "No tienes permisos para acceder a esta página."

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser or self.request.user.groups.filter(name='InventarioPermisos').exists() or self.request.user.groups.filter(name='VariosPermisos').exists()

    def handle_no_permission(self):
        return redirect('Home_User')
    
    def get(self,request, *args, **kwargs):
        empresa_id = request.GET.get('empresa_id')
        empresas = Sucursal.objects.all()
        empresaselect = Sucursal.objects.filter(id=empresa_id).first() if empresa_id else None
        
        # Filtrar productos por la empresa seleccionada
        productos = Producto.objects.filter(sucursal=empresaselect).select_related('categoria', 'local') if empresaselect else Producto.objects.none()
        
        # Crear un formulario con los productos filtrados
        form = RegistroSalidaForm()
        form.fields['producto'].queryset = productos
        
        context = {
            'empresas': empresas,
            'productos': productos,
            'form': form,
            'empresaselect': empresaselect,
        }
        return render(request, 'Inventario/gestion/RegistrarSalida.html',context)

    
    def post(self,request, *args, **kwargs):
        form = RegistroSalidaForm(request.POST)
        if form.is_valid():
            try:
                if request.user.is_superuser:
                    # Si el usuario es superusuario, se asigna el mismo usuario como encargado
                    encargado = request.user.empleado
                else:
                    # Si no es superusuario, también se asigna el empleado del usuario actual
                    encargado = request.user.empleado

                # Verificar si el usuario tiene un Empleado asociado
                if not encargado:
                    messages.error(request, 'El usuario no tiene un empleado asociado.')
                    return redirect('Inventario_Home')

                form.instance.encargado = encargado

                # Actualizar el stock del producto
                producto = form.instance.producto
                producto.stock -= form.instance.cantidad
                producto.save()
                
                # Guardar la instancia del formulario
                form.save()
                
                messages.success(request, 'Salida registrada con éxito')
            except Exception as e:
                messages.error(request, f'Ocurrió un error al procesar la salida: {e}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error en el campo {field}: {error}')

        return redirect('Inventario_Home')

class RegistrarEntradaViewHome(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')
    permission_denied_message = "No tienes permisos para acceder a esta página."

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser or self.request.user.groups.filter(name='InventarioPermisos').exists() or self.request.user.groups.filter(name='VariosPermisos').exists()

    def handle_no_permission(self):
        return redirect('Home_User')
    
    def get(self,request, *args, **kwargs):
        empresa_id = request.GET.get('empresa_id')  # Obtenemos el ID de la empresa seleccionada
        empresas = Sucursal.objects.all()  # Todas las empresas para mostrar en la lista desplegable
        empresaselect = Sucursal.objects.filter(id=empresa_id).first() if empresa_id else None  # Empresa seleccionada
        
        # Filtramos los productos por la empresa seleccionada
        productos = Producto.objects.filter(sucursal=empresaselect).select_related('categoria', 'local') if empresaselect else Producto.objects.none()

        # Creamos el formulario con los productos filtrados
        form = RegistroEntradaForm()
        form.fields['producto'].queryset = productos
        
        context = {
            'empresas': empresas,
            'productos': productos,
            'form': form,
            'empresaselect': empresaselect,
        }
        return render(request, 'Inventario/gestion/RegistrarEntrada.html',context)

    
    def post(self,request, *args, **kwargs):
        form = RegistroEntradaForm(request.POST)
        if form.is_valid():
            if not request.user.is_superuser:
                form.instance.encargado = request.user.empleado
            else:
                form.instance.encargado = request.user.empleado

            producto = form.instance.producto
            producto.stock += form.instance.cantidad
            producto.save()
            
            # Guardar la instancia del formulario
            form.save()
            messages.success(request, 'Entrada registrada con éxito')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error en el campo {field}: {error}')

        return redirect('Inventario_Home')
    
