from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from .models import Paciente
from .forms import PacienteForm


# ==========================================
# LISTAR PACIENTES
# ==========================================

def lista_pacientes(request):

    if not request.session.get('id_usuario'):

        return redirect('/')

    pacientes = Paciente.objects.all().order_by(
        '-id_paciente'
    )

    return render(

        request,

        'pacientes/lista.html',

        {

            'pacientes': pacientes

        }

    )


# ==========================================
# CREAR PACIENTE
# ==========================================

def crear_paciente(request):

    if not request.session.get('id_usuario'):

        return redirect('/')

    if request.method == 'POST':

        form = PacienteForm(request.POST)

        if form.is_valid():

            paciente = form.save(commit=False)

            # CAPTURAR ACTIVO
            activo = request.POST.get('activo')

            paciente.activo = (
                True if activo == 'True'
                else False
            )

            paciente.save()

            return redirect('/pacientes/')

    else:

        form = PacienteForm()

    return render(

        request,

        'pacientes/crear.html',

        {

            'form': form

        }

    )


# ==========================================
# EDITAR PACIENTE
# ==========================================

def editar_paciente(request, id):

    if not request.session.get('id_usuario'):

        return redirect('/')

    paciente = get_object_or_404(

        Paciente,

        id_paciente=id

    )

    if request.method == 'POST':

        form = PacienteForm(

            request.POST,

            instance=paciente

        )

        if form.is_valid():

            paciente = form.save(commit=False)

            # ACTUALIZAR ACTIVO
            activo = request.POST.get('activo')

            paciente.activo = (
                True if activo == 'True'
                else False
            )

            paciente.save()

            return redirect('/pacientes/')

    else:

        form = PacienteForm(

            instance=paciente

        )

    return render(

        request,

        'pacientes/editar.html',

        {

            'form': form,

            'paciente': paciente

        }

    )


# ==========================================
# ELIMINAR LOGICO
# ==========================================

def eliminar_paciente(request, id):

    paciente = get_object_or_404(

        Paciente,

        id_paciente=id

    )

    paciente.activo = False

    paciente.save()

    return redirect('/pacientes/')