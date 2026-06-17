from django.db import models

from apps.pacientes.models import Paciente
from apps.citas.models import Cita
from apps.login.models import Usuario


class Consulta(models.Model):

    id_consulta = models.AutoField(
        primary_key=True
    )

    id_paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        db_column='id_paciente'
    )

    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        db_column='id_usuario'
    )

    id_cita = models.ForeignKey(
        Cita,
        on_delete=models.CASCADE,
        db_column='id_cita'
    )

    fecha_consulta = models.DateTimeField(
        auto_now_add=True
    )

    motivo_consulta = models.TextField()

    diagnostico = models.TextField()

    tratamiento = models.TextField()

    observaciones = models.TextField(
        blank=True,
        null=True
    )

    class Meta:

        db_table = 'consulta'

    def __str__(self):
    
        return f'Consulta de {self.id_paciente.nombres} {self.id_paciente.apellidos}'