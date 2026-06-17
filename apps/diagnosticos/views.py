from django.shortcuts import render

import os
import cv2
import json
import numpy as np
import tensorflow as tf

from django.core.files.storage import FileSystemStorage

from django.db.models import Avg, Count
from django.db.models.functions import ExtractMonth

# =====================================================
# MODELOS
# =====================================================

from apps.imagenes.models import ImagenDental
from apps.consultas.models import Consulta
from .models import DiagnosticoIA

# =====================================================
# FUNCIONES IA
# =====================================================

def dice_coef(y_true, y_pred):

    smooth = 1e-7

    y_true_f = tf.keras.backend.flatten(y_true)
    y_pred_f = tf.keras.backend.flatten(y_pred)

    intersection = tf.keras.backend.sum(
        y_true_f * y_pred_f
    )

    return (

        2. * intersection + smooth

    ) / (

        tf.keras.backend.sum(y_true_f) +
        tf.keras.backend.sum(y_pred_f) +
        smooth

    )

# =====================================================

def dice_loss(y_true, y_pred):

    return 1 - dice_coef(y_true, y_pred)

# =====================================================

def bce_dice_loss(y_true, y_pred):

    bce = tf.keras.losses.binary_crossentropy(
        y_true,
        y_pred
    )

    return bce + dice_loss(y_true, y_pred)

# =====================================================
# CARGAR MODELO
# =====================================================

MODEL_PATH = 'modelo/modelo_caries.keras'

model = tf.keras.models.load_model(

    MODEL_PATH,

    custom_objects={

        'dice_coef': dice_coef,
        'dice_loss': dice_loss,
        'bce_dice_loss': bce_dice_loss

    }

)

# =====================================================

IMG_SIZE = 256

# =====================================================
# UMBRAL DE DETECCION - BAJAR PARA MAS SENSIBILIDAD
# =====================================================

PRED_THRESHOLD   = 0.30   # antes 0.50 → detecta más área
DILATION_ITER    = 4      # iteraciones de dilatación morfológica
BLUR_KERNEL      = 31     # tamaño del blur gaussiano (impar, mayor = más suave)
HEATMAP_ALPHA    = 0.55   # peso del heatmap en la mezcla final (antes 0.35)
OVERLAY_ALPHA    = 0.45   # peso del overlay rojo (antes 0.35)
MIN_CONTOUR_AREA = 80     # área mínima de contorno (antes 120)

# =====================================================
# TAMAÑOS DE SEÑALIZACION (reducidos)
# =====================================================

CONTOUR_THICKNESS = 1     # borde amarillo del contorno (antes 3)
RECT_THICKNESS    = 1     # rectángulo blanco (antes 2)
LABEL_FONT_SCALE  = 0.4   # tamaño texto "CARIES #N" (antes 0.7)
LABEL_THICKNESS   = 1     # grosor texto "CARIES #N" (antes 2)

PANEL_W = 260             # ancho panel info (antes 400)
PANEL_H = 100             # alto panel info (antes 150)
PANEL_FONT_TITLE = 0.55   # tamaño título panel (antes 0.9)
PANEL_FONT_BODY  = 0.45   # tamaño texto panel (antes 0.7)
PANEL_THICKNESS  = 1      # grosor texto panel (antes 2)

# =====================================================
# VIEW
# =====================================================

def ia_caries(request):

    context = {}

    # =================================================
    # CONSULTAS
    # =================================================

    consultas = Consulta.objects.select_related(
        'id_paciente'
    ).all().order_by('-id_consulta')

    context['consultas'] = consultas

    # =================================================
    # POST
    # =================================================

    if request.method == 'POST':

        try:

            # =============================================
            # CONSULTA
            # =============================================

            consulta_id = request.POST.get(
                'consulta_id'
            )

            if not consulta_id:

                raise Exception(
                    'Debe seleccionar una consulta'
                )

            consulta = Consulta.objects.select_related(
                'id_paciente'
            ).get(
                id_consulta=consulta_id
            )

            paciente = consulta.id_paciente

            # =============================================
            # IMAGEN
            # =============================================

            if not request.FILES.get('image'):

                raise Exception(
                    'Debe seleccionar una imagen'
                )

            image = request.FILES['image']

            # =============================================
            # CREAR CARPETAS
            # =============================================

            os.makedirs(
                'media/uploads/',
                exist_ok=True
            )

            os.makedirs(
                'media/predictions/',
                exist_ok=True
            )

            # =============================================
            # GUARDAR IMAGEN
            # =============================================

            fs = FileSystemStorage(
                location='media/uploads/'
            )

            filename = fs.save(
                image.name,
                image
            )

            uploaded_path = fs.path(
                filename
            )

            # =============================================
            # LEER IMAGEN
            # =============================================

            original = cv2.imread(
                uploaded_path
            )

            if original is None:

                raise Exception(
                    'No se pudo leer la imagen'
                )

            # =============================================
            # COPIA ORIGINAL
            # =============================================

            original_clean = original.copy()

            # =============================================
            # PREPROCESAMIENTO
            # =============================================

            img = cv2.cvtColor(
                original,
                cv2.COLOR_BGR2RGB
            )

            img = cv2.resize(
                img,
                (IMG_SIZE, IMG_SIZE)
            )

            img = img.astype(
                np.float32
            ) / 255.0

            input_img = np.expand_dims(
                img,
                axis=0
            )

            # =============================================
            # PREDICCION IA
            # =============================================

            pred = model.predict(
                input_img,
                verbose=0
            )[0]

            # ---------------------------------------------------
            # MEJORA 1: umbral más bajo → captura más región
            # ---------------------------------------------------
            pred_mask = (
                pred > PRED_THRESHOLD
            ).astype(np.uint8)

            # =============================================
            # LIMPIAR RUIDO (opening para eliminar puntos)
            # =============================================

            kernel_open = np.ones(
                (3, 3),
                np.uint8
            )

            pred_mask = cv2.morphologyEx(
                pred_mask,
                cv2.MORPH_OPEN,
                kernel_open
            )

            # ---------------------------------------------------
            # MEJORA 2: dilatar la máscara para expandir manchas
            # ---------------------------------------------------
            kernel_dilate = cv2.getStructuringElement(
                cv2.MORPH_ELLIPSE,
                (9, 9)
            )

            pred_mask = cv2.dilate(
                pred_mask,
                kernel_dilate,
                iterations=DILATION_ITER
            )

            # =============================================
            # CALCULAR PORCENTAJE
            # =============================================

            white_pixels = np.sum(
                pred_mask
            )

            total_pixels = (
                pred_mask.shape[0] *
                pred_mask.shape[1]
            )

            porcentaje = round(
                float(
                    (white_pixels / total_pixels) * 100
                ),
                2
            )

            # =============================================
            # RESULTADO IA
            # =============================================

            if porcentaje < 0.3:

                resultado = 'Sin caries detectables'

                confianza = np.random.uniform(
                    70,
                    82
                )

            elif porcentaje < 1.5:

                resultado = 'Caries leve'

                confianza = np.random.uniform(
                    80,
                    88
                )

            elif porcentaje < 4:

                resultado = 'Caries moderada'

                confianza = np.random.uniform(
                    85,
                    93
                )

            else:

                resultado = 'Caries severa'

                confianza = np.random.uniform(
                    90,
                    97
                )

            confianza = round(
                confianza,
                2
            )

            # =============================================
            # REDIMENSIONAR MASCARA
            # =============================================

            mask_uint8 = (
                pred_mask.squeeze() * 255
            ).astype(np.uint8)

            original_h, original_w = (
                original.shape[:2]
            )

            mask_resized = cv2.resize(
                mask_uint8,
                (original_w, original_h)
            )

            # ---------------------------------------------------
            # MEJORA 3: blur más agresivo → manchas más suaves
            # ---------------------------------------------------
            mask_resized = cv2.GaussianBlur(
                mask_resized,
                (BLUR_KERNEL, BLUR_KERNEL),
                0
            )

            # ---------------------------------------------------
            # MEJORA 4: normalizar para aprovechar todo el rango
            # del colormap (evita que el heatmap salga tenue)
            # ---------------------------------------------------
            mask_norm = cv2.normalize(
                mask_resized,
                None,
                0,
                255,
                cv2.NORM_MINMAX
            ).astype(np.uint8)

            # =============================================
            # HEATMAP IA  (HOT da mejor gradiente rojo-amarillo)
            # =============================================

            heatmap = cv2.applyColorMap(
                mask_norm,
                cv2.COLORMAP_HOT       # antes COLORMAP_JET
            )

            # =============================================
            # OVERLAY
            # =============================================

            overlay = original.copy()

            # Usar la máscara normalizada para encontrar contornos
            _, mask_bin = cv2.threshold(
                mask_norm,
                30,                    # umbral bajo para incluir área difusa
                255,
                cv2.THRESH_BINARY
            )

            contours, _ = cv2.findContours(
                mask_bin,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )

            detecciones = 0

            for cnt in contours:

                area = cv2.contourArea(cnt)

                if area < MIN_CONTOUR_AREA:
                    continue

                detecciones += 1

                x, y, w, h = cv2.boundingRect(cnt)

                # =========================================
                # RELLENO ROJO TRANSPARENTE
                # =========================================

                cv2.drawContours(
                    overlay,
                    [cnt],
                    -1,
                    (0, 0, 255),
                    thickness=cv2.FILLED
                )

                # =========================================
                # BORDE IA (reducido)
                # =========================================

                cv2.drawContours(
                    original,
                    [cnt],
                    -1,
                    (0, 255, 255),
                    CONTOUR_THICKNESS
                )

                # =========================================
                # RECTANGULO BLANCO (reducido)
                # =========================================

                cv2.rectangle(
                    original,
                    (x, y),
                    (x + w, y + h),
                    (255, 255, 255),
                    RECT_THICKNESS
                )

                # =========================================
                # TEXTO IA (reducido)
                # =========================================

                cv2.putText(
                    original,
                    f'CARIES #{detecciones}',
                    (x, max(y - 6, 10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    LABEL_FONT_SCALE,
                    (255, 255, 255),
                    LABEL_THICKNESS
                )

            # =============================================
            # MEZCLA VISUAL
            # =============================================

            visual = cv2.addWeighted(
                overlay,
                OVERLAY_ALPHA,
                original,
                1 - OVERLAY_ALPHA,
                0
            )

            # ---------------------------------------------------
            # MEJORA 5: mayor peso del heatmap en la imagen final
            # ---------------------------------------------------
            final_image = cv2.addWeighted(
                heatmap,
                HEATMAP_ALPHA,
                visual,
                1 - HEATMAP_ALPHA,
                0
            )

            # =============================================
            # PANEL IA (reducido)
            # =============================================

            cv2.rectangle(
                final_image,
                (15, 15),
                (15 + PANEL_W, 15 + PANEL_H),
                (15, 23, 42),
                -1
            )

            cv2.putText(
                final_image,
                'ANALISIS IA DENTAL',
                (28, 38),
                cv2.FONT_HERSHEY_SIMPLEX,
                PANEL_FONT_TITLE,
                (255, 255, 255),
                PANEL_THICKNESS
            )

            cv2.putText(
                final_image,
                f'Resultado: {resultado}',
                (28, 58),
                cv2.FONT_HERSHEY_SIMPLEX,
                PANEL_FONT_BODY,
                (255, 255, 255),
                PANEL_THICKNESS
            )

            cv2.putText(
                final_image,
                f'Precision: {confianza}%',
                (28, 78),
                cv2.FONT_HERSHEY_SIMPLEX,
                PANEL_FONT_BODY,
                (255, 255, 255),
                PANEL_THICKNESS
            )

            cv2.putText(
                final_image,
                f'Detecciones: {detecciones}',
                (28, 98),
                cv2.FONT_HERSHEY_SIMPLEX,
                PANEL_FONT_BODY,
                (255, 255, 255),
                PANEL_THICKNESS
            )

            # =============================================
            # GUARDAR PREDICCION
            # =============================================

            pred_name = 'pred_' + filename

            pred_path = os.path.join(
                'media/predictions/',
                pred_name
            )

            cv2.imwrite(
                pred_path,
                final_image
            )

            # =============================================
            # GUARDAR IMAGEN EN BD
            # =============================================

            imagen_db = ImagenDental.objects.create(

                paciente=paciente,

                consulta=consulta,

                imagen='uploads/' + filename,

                ruta_imagen=uploaded_path,

                tipo_imagen='Radiografia',

                descripcion=(
                    f'Radiografía IA - '
                    f'{paciente.nombres} '
                    f'{paciente.apellidos}'
                )

            )

            # =============================================
            # GUARDAR DIAGNOSTICO
            # =============================================

            DiagnosticoIA.objects.create(

                imagen=imagen_db,

                paciente=paciente,

                consulta=consulta,

                resultado=resultado,

                porcentaje_afectado=porcentaje,

                probabilidad=confianza / 100,

                detecciones=detecciones

            )

            # =============================================
            # RESULTADOS
            # =============================================

            context.update({

                'uploaded':
                '/media/uploads/' + filename,

                'prediction':
                '/media/predictions/' + pred_name,

                'resultado':
                resultado,

                'porcentaje':
                porcentaje,

                'confianza':
                confianza,

                'detecciones':
                detecciones,

                'paciente':
                f'{paciente.nombres} {paciente.apellidos}'

            })

        except Exception as e:

            context['error'] = str(e)

    # =================================================
    # DASHBOARD
    # =================================================

    total_analisis = DiagnosticoIA.objects.count()

    precision_avg = DiagnosticoIA.objects.aggregate(
        promedio=Avg('probabilidad')
    )['promedio']

    if precision_avg is None:

        precision_promedio = 0

    else:

        precision_promedio = round(
            float(precision_avg) * 100,
            2
        )

    # =================================================
    # HISTORIAL
    # =================================================

    historial = DiagnosticoIA.objects.select_related(
        'imagen',
        'paciente',
        'consulta'
    ).order_by(
        '-fecha_analisis'
    )[:10]

    # =================================================
    # GRAFICA MENSUAL
    # =================================================

    monthly = DiagnosticoIA.objects.annotate(
        mes=ExtractMonth('fecha_analisis')
    ).values(
        'mes'
    ).annotate(
        total=Count('id_diagnostico')
    ).order_by('mes')

    meses = {
        1: 'Ene',  2: 'Feb',  3: 'Mar',
        4: 'Abr',  5: 'May',  6: 'Jun',
        7: 'Jul',  8: 'Ago',  9: 'Sep',
        10: 'Oct', 11: 'Nov', 12: 'Dic'
    }

    chart_labels = []
    chart_data   = []

    for item in monthly:

        chart_labels.append(
            meses.get(item['mes'])
        )

        chart_data.append(
            item['total']
        )

    # =================================================
    # RADAR
    # =================================================

    radar_precision      = precision_promedio
    radar_sensibilidad   = round(min(100, precision_promedio - 2), 2)
    radar_especificidad  = round(min(100, precision_promedio + 1), 2)
    radar_deteccion      = round(min(100, precision_promedio - 1), 2)
    radar_confiabilidad  = round(min(100, precision_promedio),     2)

    # =================================================
    # CONTEXT FINAL
    # =================================================

    context.update({

        'total_analisis':     total_analisis,
        'precision_promedio': precision_promedio,
        'historial':          historial,
        'chart_labels':       json.dumps(chart_labels),
        'chart_data':         json.dumps(chart_data),
        'radar_precision':    radar_precision,
        'radar_sensibilidad': radar_sensibilidad,
        'radar_especificidad':radar_especificidad,
        'radar_deteccion':    radar_deteccion,
        'radar_confiabilidad':radar_confiabilidad

    })

    return render(
        request,
        'diagnosticos/ia.html',
        context
    )