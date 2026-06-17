from django.db import models
from datetime import date

class Paciente(models.Model):
    
    id_paciente = models.AutoField(
        primary_key=True
    )

    nombres = models.CharField(
        max_length=120
    )

    apellidos = models.CharField(
        max_length=120
    )

    fecha_nacimiento = models.DateField()

    sexo = models.CharField(
        max_length=10,
        null=True,
        blank=True
    )
    @property
    def edad(self):
        hoy = date.today()

        edad = hoy.year - self.fecha_nacimiento.year

        if (
            (hoy.month, hoy.day)
            <
            (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        ):
            edad -= 1

        return edad

    direccion = models.TextField(
        null=True,
        blank=True
    )

    telefono_padre = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    nombre_padre = models.CharField(
        max_length=120,
        null=True,
        blank=True
    )

    correo_padre = models.CharField(
        max_length=120,
        null=True,
        blank=True
    )

    fecha_registro = models.DateTimeField(
        auto_now_add=True
    )

    activo = models.BooleanField(default=True)

    class Meta:

        db_table = 'paciente'

    def __str__(self):

        return f'{self.nombres} {self.apellidos}'