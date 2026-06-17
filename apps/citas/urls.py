from django.urls import path

from . import views
from .views import lista_citas

urlpatterns = [
      path(
        '',
        lista_citas
    ),

    path(
        '',
        views.lista_citas
    ),

    path(
        'crear/',
        views.crear_cita
    ),

    path(
        'editar/<int:id>/',
        views.editar_cita
    ),
    

]   