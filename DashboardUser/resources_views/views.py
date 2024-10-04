from django.shortcuts import render
from DashboardAdmin.models import Recurso,CategoriaRecurso
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
import os
 
class RecursosHomeViewUser(LoginRequiredMixin, View):    
    def get(self, request, *args, **kwargs):
        Categoria_Recurso  = CategoriaRecurso.objects.all()
        recursos = Recurso.objects.all()
        
        context ={
            'url': 'Recursos',
            'sourcecat': Categoria_Recurso,
            'recursos': recursos,
            'AZURE_SAS_TOKEN': os.environ.get('AZURE_SAS_TOKEN','')
        }
        return render(request, 'User/resources/Home.html', context)