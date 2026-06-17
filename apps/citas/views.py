from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from .models import Cita
from .forms import CitaForm
from apps.login.models import Usuario
from apps.pacientes.models import Paciente

def lista_citas(request):
    
    if not request.session.get('id_usuario'):

        return redirect('/')

    # CREAR
    if request.method == 'POST':

        form = CitaForm(request.POST)

        if form.is_valid():

            cita = form.save(commit=False)

            usuario = Usuario.objects.get(
                id_usuario=request.session['id_usuario']
            )

            cita.id_usuario = usuario

            cita.save()

            return redirect('/citas/')

    else:

        form = CitaForm()

    citas = Cita.objects.all().order_by('-id_cita')

    # =================================================
    # CONTEOS PARA TARJETAS RESUMEN
    # =================================================

    total_programadas = citas.filter(estado='programada').count()
    total_completadas = citas.filter(estado='completada').count()
    total_canceladas  = citas.filter(estado='cancelada').count()

    return render(
        request,
        'citas/lista.html',
        {
            'citas': citas,
            'form': form,
            'total_programadas': total_programadas,
            'total_completadas': total_completadas,
            'total_canceladas': total_canceladas,
        }
    )


def crear_cita(request):

    if not request.session.get('id_usuario'):

        return redirect('/')

    if request.method == 'POST':

        form = CitaForm(request.POST)

        if form.is_valid():

            cita = form.save(commit=False)

            cita.id_usuario_id = request.session['id_usuario']

            cita.save()

            return redirect('/citas/')

    else:

        form = CitaForm()

    return render(

        request,

        'citas/crear.html',

        {

            'form': form

        }

    )


def editar_cita(request, id):
    
    if not request.session.get('id_usuario'):

        return redirect('/')

    cita = get_object_or_404(
        Cita,
        id_cita=id
    )

    if request.method == 'POST':

        paciente_id = request.POST.get('id_paciente')

        fecha_cita = request.POST.get('fecha_cita')

        estado = request.POST.get('estado')

        observacion = request.POST.get('observacion')

        # VALIDAR PACIENTE
        if paciente_id:

            cita.id_paciente = Paciente.objects.get(
                id_paciente=paciente_id
            )

        # USUARIO DE LA SESION
        usuario = Usuario.objects.get(
            id_usuario=request.session['id_usuario']
        )

        cita.id_usuario = usuario

        cita.fecha_cita = fecha_cita

        cita.estado = estado

        cita.observacion = observacion

        cita.save()

        return redirect('/citas/')

    pacientes = Paciente.objects.filter(
        activo=True
    )

    return render(
        request,
        'citas/editar.html',
        {
            'cita': cita,
            'pacientes': pacientes
        }
    )