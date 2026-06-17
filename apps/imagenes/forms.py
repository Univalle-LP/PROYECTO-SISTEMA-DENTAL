from django import forms

from .models import ImagenDental

from apps.consultas.models import Consulta


class ImagenDentalForm(forms.ModelForm):

    class Meta:

        model = ImagenDental

        fields = [

            'consulta',
            'imagen',
            'tipo_imagen',
            'descripcion'

        ]

        widgets = {

            'consulta': forms.Select(

                attrs={

                    'class': 'form-select'

                }

            ),

            'imagen': forms.FileInput(

                attrs={

                    'class': 'form-control'

                }

            ),

            'tipo_imagen': forms.Select(

                choices=[

                    ('Radiografía', 'Radiografía'),
                    ('Fotografía', 'Fotografía'),
                    ('Tomografía', 'Tomografía')

                ],

                attrs={

                    'class': 'form-select'

                }

            ),

            'descripcion': forms.Textarea(

                attrs={

                    'class': 'form-control',
                    'rows': 3

                }

            )

        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['consulta'].queryset = Consulta.objects.all()

        self.fields['consulta'].label_from_instance = lambda obj: (

            f'{obj.id_paciente.nombres} '
            f'{obj.id_paciente.apellidos} '
            f'- Consulta #{obj.id_consulta}'

        )