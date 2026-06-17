from django import forms

from .models import Paciente


class PacienteForm(forms.ModelForm):

    class Meta:

        model = Paciente

        fields = [

            'nombres',
            'apellidos',
            'fecha_nacimiento',
            'sexo',
            'direccion',
            'telefono_padre',
            'nombre_padre',
            'correo_padre'

        ]

        widgets = {

            'nombres': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'apellidos': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'fecha_nacimiento': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),

            'sexo': forms.Select(
                choices=[
                    ('Masculino', 'Masculino'),
                    ('Femenino', 'Femenino')
                ],
                attrs={
                    'class': 'form-select'
                }
            ),

            'direccion': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3
                }
            ),

            'telefono_padre': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'nombre_padre': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'correo_padre': forms.EmailInput(
                attrs={
                    'class': 'form-control'
                }
            ),

        }