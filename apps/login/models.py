from django.db import models


class Usuario(models.Model):

    id_usuario = models.AutoField(
        primary_key=True
    )

    username = models.CharField(
        max_length=50,
        unique=True
    )

    password = models.CharField(
        max_length=255
    )

    nombre = models.CharField(
        max_length=100
    )

    apellido = models.CharField(
        max_length=100
    )

    email = models.EmailField(
        max_length=120,
        null=True,
        blank=True
    )

    telefono = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    fecha_registro = models.DateTimeField()

    activo = models.BooleanField(
        default=True
    )

    class Meta:

        managed = False

        db_table = 'usuario'


    def __str__(self):

        return self.username


class LogLogin(models.Model):

    id_log = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=50)
    fecha = models.DateTimeField(auto_now_add=True)
    exitoso = models.BooleanField()

    class Meta:
        db_table = 'log_login'