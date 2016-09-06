# -*- coding: utf-8 -*-
import json
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from actas.stream_datas import get_respuestas

from .libs import validar_acta_json, validar_cedulas_participantes, guardar_acta, obtener_config, get_participantes, generar_propuesta_docx

from .models import ConfiguracionEncuentro


def index(request):
    return render(request, 'index.html')


def lista(request):
    return render(request, 'lista.html')


@ensure_csrf_cookie
def subir(request):
    return render(request, 'subir.html')


def acta_base(request,id):
    config = obtener_config()

    config_acta_base = {
        'min_participantes': config['participantes_min'],
        'max_participantes': config['participantes_max'],
        'participante_organizador': {},
        'participantes': [{} for _ in range(config['participantes_min']-1)]

    }

    # acta['itemsGroups'] = [g.to_dict() for g in Tema.objects.all().order_by('orden')]
    config_acta = ConfiguracionEncuentro.objects.get(pk=int(id)).to_dict()
    config_acta_base.update(config_acta)

    return JsonResponse(config_acta_base)


@transaction.atomic
def subir_validar(request):
    acta, errores = validar_acta_json(request)

    if len(errores) > 0:
        return JsonResponse({'status': 'error', 'mensajes': errores}, status=400)

    return JsonResponse({'status': 'success', 'mensajes': ['El acta ha sido validada exitosamente.']})


@transaction.atomic
def subir_confirmar(request):
    acta, errores = validar_acta_json(request)

    if len(errores) > 0:
        return JsonResponse({'status': 'error', 'mensajes': errores}, status=400)

    errores = validar_cedulas_participantes(acta)

    if len(errores) == 0:
        guardar_acta(acta)
        return JsonResponse({'status': 'success', 'mensajes': ['El acta ha sido ingresada exitosamente.']})

    return JsonResponse({'status': 'error', 'mensajes': errores}, status=400)

def bajar_propuesta_docx(request):
    acta = request.body.decode('utf-8')

    try:
        acta = json.loads(acta)
    except ValueError:
        return (None, 'Acta inválida.',)

    docx = generar_propuesta_docx(acta)

    # descarga de documento
    length = docx.tell()
    docx.seek(0)
    response = HttpResponse(
        docx.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = 'attachment; filename=propuesta.docx'
    response['Content-Length'] = length
    return response

def bajar_participantes(request):
    return get_participantes(request)

def bajar_propuestas(request):
    return get_respuestas(request)
