from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from apps.pacientes.models import Paciente
from apps.citas.models import Cita
from apps.login.models import Usuario

from .models import Consulta
from .forms import ConsultaForm


def lista_consultas(request):

    if not request.session.get('id_usuario'):

        return redirect('/')

    if request.method == 'POST':

        form = ConsultaForm(request.POST)

        if form.is_valid():

            consulta = form.save(commit=False)

            consulta.id_usuario = Usuario.objects.get(
                id_usuario=request.session['id_usuario']
            )

            consulta.save()

            return redirect('/consultas/')

        else:

            print(form.errors)

    else:

        form = ConsultaForm()

    consultas = Consulta.objects.all().order_by(
        '-id_consulta'
    )

    return render(
        request,
        'consultas/lista.html',
        {
            'consultas': consultas,
            'form': form
        }
    )

def editar_consulta(request, id):

    consulta = get_object_or_404(
        Consulta,
        id_consulta=id
    )

    if request.method == 'POST':

        consulta.fecha_consulta = request.POST.get(
            'fecha_consulta'
        )

        consulta.motivo_consulta = request.POST.get(
            'motivo_consulta'
        )

        consulta.diagnostico = request.POST.get(
            'diagnostico'
        )

        consulta.tratamiento = request.POST.get(
            'tratamiento'
        )

        consulta.save()

        return redirect('/consultas/')