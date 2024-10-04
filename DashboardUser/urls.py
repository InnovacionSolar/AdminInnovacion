from django.urls import path
from .views import EmpleadoLoginView,DashboardUser, ProfileHomeView, NotasHomeView, AsistenciaHomeView,EmpleadoUpdateView
from django.contrib.auth.views import LogoutView
from .performance_views.views import PerformanceView, DetailActividadView
from DashboardUser.resources_views.views import RecursosHomeViewUser
from DashboardAdmin.inventario_views.views import InventarioHomeView
from DashboardAdmin.informes_views.views import InformesHomeView
from DashboardAdmin.source_views.views import RecursosHomeView
from DashboardAdmin.rendimiento_views.views import RendimientoViewHome
from DashboardAdmin.asistencia_views.views import AsistenciaViewHome
from DashboardAdmin.views import EmpleadoView
from .horario_views.views import *

urlpatterns = [
    path('', DashboardUser.as_view(), name='Home_User'),
    #Full Login View
    
    path('login/', EmpleadoLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Paths de dashboard user
    path('profile/', ProfileHomeView.as_view(), name='Profile'),
    path('profile/update/', EmpleadoUpdateView.as_view(), name='ProfileUpdate'),
    
    #Paths de asistencias
    path('asistencias/', AsistenciaHomeView.as_view(), name='Asistencia'),
    path('salida/', AsistenciaHomeView.as_view(), name='Salida'),

    #Rendimiento
    path('performance/', PerformanceView.as_view(), name='Performance_Home'),
    path('performance/preview/<int:id>/', DetailActividadView.as_view(), name='Performance_Detail'),
    
    #Resoures
    path('resources/usuarios/', RecursosHomeViewUser.as_view(), name='Recursos_Usuarios'),
    
    #Path de inventario 
    path('inventario/', InventarioHomeView.as_view(), name='Inventario_UserHome'),
    
    #Path de informes 
    path('Informes/', InformesHomeView.as_view(), name='Informes_UserHome'),
    path('recursos/', RecursosHomeView.as_view(), name='Recursos_UserHome'),
    path('rendimiento/', RendimientoViewHome.as_view(), name='Rendimiento_UserHome'),
    path('gestion/', AsistenciaViewHome.as_view(), name='gestion_Userview'),

    #Path de empleados 
    path('empleados/', EmpleadoView.as_view(), name='Empleados_UserHome'),

    #horarios 
    path('horario/', HorarioHomeView.as_view(), name='Horario_Home'),

    #notas 
    path('notas/', NotasHomeView.as_view(), name='Notas_Home')
    ]
