from django import forms

from .models import Cita


class CitaForm(forms.ModelForm):

    class Meta:

        model = Cita

        fields = [

            'id_paciente',
            'fecha_cita',
            'estado',
            'observacion'

        ]

        widgets = {

            'id_paciente': forms.Select(

                attrs={

                    'class': 'form-select'

                }

            ),

            'fecha_cita': forms.DateTimeInput(

                attrs={

                    'class': 'form-control',
                    'type': 'datetime-local'

                }

            ),

            'estado': forms.Select(

                choices=[

                    ('programada', 'Programada'),
                    ('completada', 'Completada'),
                    ('cancelada', 'Cancelada')

                ],

                attrs={

                    'class': 'form-select'

                }

            ),

            'observacion': forms.Textarea(

                attrs={

                    'class': 'form-control',
                    'rows': 3

                }

            )

        }