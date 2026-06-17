from django.shortcuts import render, redirect

from django.db.models import Count, Avg
from django.db.models.functions import ExtractMonth
from django.utils import timezone

# =====================================================
# IMPORTAR MODELOS
# =====================================================

from apps.pacientes.models import Paciente
from apps.consultas.models import Consulta
from apps.citas.models import Cita
from apps.diagnosticos.models import DiagnosticoIA

# =====================================================
# DASHBOARD
# =====================================================

def dashboard_view(request):

    # ================================================
    # VALIDAR LOGIN
    # ================================================

    if not request.session.get('id_usuario'):

        return redirect('/')

    # ================================================
    # TARJETAS SUPERIORES
    # ================================================

    total_pacientes = Paciente.objects.count()

    total_consultas = Consulta.objects.count()

    hoy = timezone.now().date()

    citas_hoy = Cita.objects.filter(

        fecha_cita__date=hoy

    ).count()

    # ================================================
    # PRECISION IA
    # ================================================

    precision = DiagnosticoIA.objects.aggregate(

        promedio=Avg('probabilidad')

    )['promedio']

    if precision:

        precision_ia = round(

            precision * 100,

            2

        )

    else:

        precision_ia = 0

    # ================================================
    # PACIENTES RECIENTES
    # ================================================

    pacientes = Paciente.objects.all().order_by(

        '-id_paciente'

    )[:8]

    # ================================================
    # DIAGNOSTICOS RECIENTES
    # ================================================

    diagnosticos = DiagnosticoIA.objects.all().order_by(

        '-fecha_analisis'

    )[:5]

    # ================================================
    # GRAFICO CONSULTAS POR MES
    # ================================================

    consultas_mes = Consulta.objects.annotate(

        mes=ExtractMonth('fecha_consulta')

    ).values(

        'mes'

    ).annotate(

        total=Count('id_consulta')

    ).order_by('mes')

    meses_dict = {

        1: 'Ene',
        2: 'Feb',
        3: 'Mar',
        4: 'Abr',
        5: 'May',
        6: 'Jun',
        7: 'Jul',
        8: 'Ago',
        9: 'Sep',
        10: 'Oct',
        11: 'Nov',
        12: 'Dic'

    }

    meses = []
    consultas_data = []

    for item in consultas_mes:

        meses.append(

            meses_dict.get(item['mes'])

        )

        consultas_data.append(

            item['total']

        )

    # ================================================
    # CONTEXT
    # ================================================

    context = {

        'total_pacientes': total_pacientes,

        'total_consultas': total_consultas,

        'citas_hoy': citas_hoy,

        'precision_ia': precision_ia,

        'pacientes': pacientes,

        'diagnosticos': diagnosticos,

        'meses': meses,

        'consultas_mes': consultas_data

    }

    # ================================================
    # RENDER
    # ================================================

    return render(

        request,

        'dashboard/dashboard.html',

        context

    )