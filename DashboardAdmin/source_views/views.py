from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from ..models import Recurso, CategoriaRecurso
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import os
from ..forms import RecursoFormCategoria, RecursosForm

class RecursosHomeView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')
    permission_denied_message = "No tienes permisos para acceder a esta página."

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser or self.request.user.groups.filter(name='InformePermisos').exists() or self.request.user.groups.filter(name='VariosPermisos').exists()

    def handle_no_permission(self):
        return redirect('Home_User')

    def get(self, request, *args, **kwargs):
        Categoria_Recurso = CategoriaRecurso.objects.all()
        recursos = Recurso.objects.all()

        tiene_permisos_informe = request.user.groups.filter(name='InformePermisos').exists() or self.request.user.groups.filter(name='VariosPermisos').exists()
        context = {
            'url': 'Recursos',
            'sourcecat': Categoria_Recurso,
            'formcategoria': RecursoFormCategoria(),
            'formrecursos': RecursosForm(),
            'messages': messages.get_messages(request),
            'recursos': recursos,
            'tiene_permisos_informe': tiene_permisos_informe,
            'AZURE_SAS_TOKEN': os.environ.get('AZURE_SAS_TOKEN', '')
        }
        return render(request, 'Recursos/Recursos.html', context)

    def post(self, request, *args, **kwargs):
        if 'categoriarecuros_submit' in request.POST:
            form = RecursoFormCategoria(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Categoria de recurso creada con éxito')
            else:
                messages.error(request, 'Error al crear la categoria de recurso')
        elif 'recursos_submit' in request.POST:
            form = RecursosForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Recurso creado con éxito')
            else:
                messages.error(request, 'Error al crear el recurso')
        return redirect('Recursos_Home')