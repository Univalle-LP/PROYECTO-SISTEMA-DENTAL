from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from apps.pacientes.models import Paciente
from apps.consultas.models import Consulta
from .models import ImagenDental
from .forms import ImagenDentalForm


def lista_imagenes(request):

    if not request.session.get('id_usuario'):

        return redirect('/')

    if request.method == 'POST':

        form = ImagenDentalForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            return redirect('/imagenes/')

        else:

            print(form.errors)

    else:

        form = ImagenDentalForm()

    imagenes = ImagenDental.objects.all().order_by(
        '-id_imagen'
    )

    return render(
        request,
        'imagenes/lista.html',
        {
            'imagenes': imagenes,
            'form': form
        }
    )


def editar_imagen(request, id):

    imagen = get_object_or_404(
        ImagenDental,
        id_imagen=id
    )

    if request.method == 'POST':

        imagen.tipo_imagen = request.POST.get(
            'tipo_imagen'
        )

        imagen.descripcion = request.POST.get(
            'descripcion'
        )

        if request.FILES.get('imagen'):

            imagen.imagen = request.FILES.get(
                'imagen'
            )

        imagen.save()

        return redirect('/imagenes/')