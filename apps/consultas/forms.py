from django import forms

from .models import Consulta

from apps.citas.models import Cita


class ConsultaForm(forms.ModelForm):

    class Meta:

        model = Consulta

        fields = [

            'id_paciente',
            'id_cita',
            'motivo_consulta',
            'diagnostico',
            'tratamiento'

        ]

        widgets = {

            'id_paciente': forms.Select(

                attrs={

                    'class': 'form-select'

                }

            ),

            'id_cita': forms.Select(

                attrs={

                    'class': 'form-select'

                }

            ),

            'motivo_consulta': forms.Textarea(

                attrs={

                    'class': 'form-control',
                    'rows': 3

                }

            ),

            'diagnostico': forms.Textarea(

                attrs={

                    'class': 'form-control',
                    'rows': 3

                }

            ),

            'tratamiento': forms.Textarea(

                attrs={

                    'class': 'form-control',
                    'rows': 3

                }

            )

        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['id_cita'].queryset = Cita.objects.all()

        self.fields['id_cita'].label_from_instance = lambda obj: (
            f'Paciente: {obj.id_paciente.nombres} | '
            f'Fecha: {obj.fecha_cita.strftime("%d/%m/%Y %H:%M")}'
        )