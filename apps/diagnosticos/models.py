from django.db import models

from apps.imagenes.models import ImagenDental
from apps.pacientes.models import Paciente
from apps.consultas.models import Consulta


class DiagnosticoIA(models.Model):

    id_diagnostico = models.AutoField(
        primary_key=True
    )

    imagen = models.ForeignKey(

        ImagenDental,

        on_delete=models.CASCADE,

        db_column='id_imagen'

    )

    paciente = models.ForeignKey(

        Paciente,

        on_delete=models.CASCADE,

        db_column='id_paciente'

    )

    consulta = models.ForeignKey(

        Consulta,

        on_delete=models.SET_NULL,

        db_column='id_consulta',

        null=True,
        blank=True

    )

    resultado = models.CharField(

        max_length=50

    )

    porcentaje_afectado = models.FloatField()

    probabilidad = models.FloatField()

    detecciones = models.IntegerField(
        default=0
    )

    observacion = models.TextField(

        blank=True,
        null=True

    )

    fecha_analisis = models.DateTimeField(

        auto_now_add=True

    )

    class Meta:

        db_table = 'diagnostico_ia'

    def __str__(self):

        return self.resultado