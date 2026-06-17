from django.urls import path

from . import views


urlpatterns = [

    path(
        '',
        views.lista_consultas
    ),

    path(
        'editar/<int:id>/',
        views.editar_consulta
    )

]