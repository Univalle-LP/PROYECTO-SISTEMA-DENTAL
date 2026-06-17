from django.urls import path

from .views import lista_pacientes
from .views import crear_paciente
from .views import editar_paciente
from .views import eliminar_paciente
from . import views


urlpatterns = [

    path(

        'pacientes/',

        lista_pacientes,

        name='pacientes'

    ),

    path(

        'pacientes/crear/',

        crear_paciente,

        name='crear_paciente'

    ),

    path(

        'pacientes/editar/<int:id>/',

        editar_paciente,

        name='editar_paciente'

    ),

    path(

        'pacientes/eliminar/<int:id>/',

        eliminar_paciente,

        name='eliminar_paciente'

    ),
     path(
        '',
        views.lista_pacientes,
        name='lista_pacientes'
    ),

    path(
        'crear/',
        views.crear_paciente,
        name='crear_paciente'
    ),

    path(
        'editar/<int:id>/',
        views.editar_paciente,
        name='editar_paciente'
    ),

]