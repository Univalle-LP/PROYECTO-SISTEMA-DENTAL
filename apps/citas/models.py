from django.db import models


class Cita(models.Model):

    id_cita = models.AutoField(
        primary_key=True
    )

    id_paciente = models.ForeignKey(
        'pacientes.Paciente',
        on_delete=models.CASCADE,
        db_column='id_paciente'
    )

    id_usuario = models.ForeignKey(
        'login.Usuario',
        on_delete=models.CASCADE,
        db_column='id_usuario'
    )

    fecha_cita = models.DateTimeField()

    estado = models.CharField(
        max_length=30,
        default='programada'
    )

    observacion = models.TextField(
        blank=True,
        null=True
    )

    class Meta:

        db_table = 'cita'

    def __str__(self):
    
        return f"{self.id_paciente.nombres} {self.id_paciente.apellidos} - {self.fecha_cita.strftime('%d/%m/%Y %H:%M')}"