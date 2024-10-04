from django.urls import path
from .views import *
from .source_views.views import RecursosHomeView
from .inventario_views.views import *
from .report_views.views import *
from .informes_views.views import *
from .asistencia_views.views import *
from .rendimiento_views.views import *

urlpatterns = [
    path('',HomeView.as_view(),name="Home"),
    #Full empleados path = DashboardAdmin/empleados/
    
    path('empleados/',EmpleadoView.as_view(),name="Empleados"),
    path('empleados/create/',EmpleadoCreate.as_view(),name="nuevo_empleado"),
    path('empleados/edit/<int:pk>/',EmpleadoEditView.as_view(),name="editar_empleado"),
    path('empleados/delete/<int:pk>/',DeleteEmpleadoView.as_view(),name="eliminar_empleado"),
    
    #Full Cargos path = DashboardAdmin/cargos/
    path('Gestion/', AsistenciaViewHome.as_view(), name="gestion_view"),
    path('cargos/', CargoView.as_view(),name="Cargos_Home"),
    path('cargos/edit/<int:pk>/', CargoEditView.as_view(), name="Cargos_edit"),

    
    #Full Recuros path = DashboardAdmin/recursos    
    path('recursos/', RecursosHomeView.as_view(),name="Recursos_Home"),
    
    #Full inventario path = DashboardAdmin/inventario/
    path('inventario/',InventarioHomeView.as_view(),name="Inventario_Home"),
    path('inventario/salida/',RegistrarSalidaViewHome.as_view(), name="Registrar_salida_view"),
    path('inventario/entrada/',RegistrarEntradaViewHome.as_view(), name="Registrar_entrada_view"),
    path('inventario/<int:pk>/listado/',InventarioHomeView.as_view(),name="inventario_empresa"),
    path('inventario/<int:pk>/view',InventarioDetailView.as_view(), name="Inventario_Detail"),
    path('inventario/<int:pk>/edit',InventarioEditView.as_view(), name="InventarioEditView"),
    path('inventario/<int:pk>/delete',InventarioDeleteView.as_view(), name="Inventario_delete"),
    
    
    #Full reports path /
    path('download_report/', download_report, name='download_report'),
    path('download_report/empleados',download_report_empleados, name='download_report_empleados'),
    path('asistencia/download/', AsistenciaViewHome.download_report_asistencia_day, name='asistencia_download_report'),
    path('asistencia/download/week/', AsistenciaViewHome.download_report_asistencia_week, name='asistencia_download_report_week'),
    path('asistencia/detail/<int:pk>/', AsistenciaDetailView.as_view(), name='asistencias_detail_user'),


    # Informes path / =  Informes/
    path('Informes/', InformesHomeView.as_view(), name="Informes_home"),
    path('Informes/<int:pk>/', CategoriaViewInformes.as_view(), name="Informes_categoria" ),
    
    path('Rendimiento/', RendimientoViewHome.as_view(), name='Rendimiento_home'),
    
    path('crear-notificacion/', CrearNotificacionView.as_view(), name='crear_notificacion'),

    #Full horarios path / = horarios/
    path('horarios/', HorarioCreateView.as_view(), name='horario'),
    path('empleado/<int:empleado_id>/horarios/', EmpleadoHorarioView.as_view(), name='empleado_horarios'),
    path('horarios/update/<int:pk>/', HorarioUpdateView.as_view(), name='update_horario'),
]   
