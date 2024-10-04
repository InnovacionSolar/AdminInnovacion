from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from ..models import Categoria_Informe, Informe
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import Q
from ..forms import InformeForm, CategoriaInformeForm
import os

class InformesHomeView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')
    permission_denied_message = "No tienes permisos para acceder a esta página."

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser or self.request.user.groups.filter(name='InventarioPermisos').exists() or self.request.user.groups.filter(name='InformePermisos').exists() or self.request.user.groups.filter(name='VariosPermisos').exists()

    def handle_no_permission(self):
        return redirect('Home_User')
    
    def get(self,request, *args, **kwargs):
        Categorias = Categoria_Informe.objects.all()
        form = InformeForm()
        catform = CategoriaInformeForm()
        
        search = request.GET.get('searchinfo', "")
        try:
            Informes = Informe.objects.filter(
                Q(resumen__icontains=search) | Q(documento__icontains=search)
            )
        except:
            Informes = Informe.objects.all()
        
        paginator = Paginator(Informes, 9)
        page_number = request.GET.get('page')
        products_data = paginator.get_page(page_number)

        context = {
            'url':"Informes",
            'categorias': Categorias,
            'informes': products_data,
            'form': form,
            'catform': catform,
            'AZURE_SAS_TOKEN': os.environ.get('AZURE_SAS_TOKEN', ''),

        }
        return render(request, 'Informes/Home.html',context)
    
    def post(self,request, *args,**kwargs):
        if 'informe_submit' in request.POST:
            form = InformeForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'El informe se ha subido correctamente.')
            else:
                messages.error(request, 'El informe no se ha subido correctamente.')
            return redirect('Informes_home')
        elif 'categoria_submit' in request.POST:
            catform = CategoriaInformeForm(request.POST)
            if catform.is_valid():
                catform.save()
                messages.success(request, 'La categoría se ha creado correctamente.')
            else:
                messages.error(request, 'La categoría no se ha creado correctamente.')
            return redirect('Informes_home')
        

class CategoriaViewInformes(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')
    permission_denied_message = "No tienes permisos para acceder a esta página."

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('Home_User')
    
    def get(self, request, *args, **kwargs):
        categoria = get_object_or_404(Categoria_Informe, pk=self.kwargs['pk'])
        form = InformeForm()

        informes = Informe.objects.filter(categoria=categoria)

        paginator = Paginator(informes, 12)
        category = Categoria_Informe.objects.all()
        page_number = request.GET.get('page')
        products_data = paginator.get_page(page_number)
        context = {
            'url':"Informes",
            'categoria': categoria,
            'informes': products_data,
            'categorias': category,
            'form': form,
        }
        return render(request, 'Informes/Home.html',context)