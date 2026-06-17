from django.urls import path

from . import views


urlpatterns = [

    path(
        '',
        views.lista_imagenes
    ),

    path(
        'editar/<int:id>/',
        views.editar_imagen
    ),

]