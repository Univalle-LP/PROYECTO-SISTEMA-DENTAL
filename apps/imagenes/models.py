from django.db import models

from apps.pacientes.models import Paciente
from apps.consultas.models import Consulta


class ImagenDental(models.Model):

    id_imagen = models.AutoField(
        primary_key=True
    )

    paciente = models.ForeignKey(

        Paciente,

        on_delete=models.CASCADE,

        db_column='id_paciente'

    )

    consulta = models.ForeignKey(

        Consulta,

        on_delete=models.CASCADE,

        db_column='id_consulta',

        null=True,
        blank=True

    )

    imagen = models.ImageField(

        upload_to='uploads/'

    )

    ruta_imagen = models.CharField(

        max_length=500

    )

    tipo_imagen = models.CharField(

        max_length=50

    )

    descripcion = models.TextField(

        blank=True,
        null=True

    )

    fecha_subida = models.DateTimeField(

        auto_now_add=True

    )

    class Meta:

        db_table = 'imagen_dental'

    def __str__(self):

        return f'Imagen {self.id_imagen}'