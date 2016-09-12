# -*- coding: utf-8 -*-
import json

from django.db import transaction
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
import ast
from actas.stream_datas import *

from .libs import validar_acta_json, validar_cedulas_participantes, guardar_acta, obtener_config, \
    generar_propuesta_docx, generar_pre_propuesta_docx, pre_propuesta_email

from .models import ConfiguracionEncuentro


def index(request):
    return render(request, 'index.html')


def lista(request):
    return render(request, 'lista.html')


@ensure_csrf_cookie
def subir(request):
    return render(request, 'subir.html')


def acta_base(request, id):
    config = obtener_config()

    base = {
        # 'min_participantes': config['participantes_min'],
        # 'max_participantes': config['participantes_max'],
        # 'participante_organizador': {},
        # 'participantes': [{} for _ in range(config['participantes_min'])],
        # 'memoria': '',

    }

    config_actas = ConfiguracionEncuentro.objects.filter(pk=int(id))

    if len(config_actas) == 0:
        return JsonResponse({}, status=404)

    base.update(config_actas[0].get_configuration())

    return JsonResponse(base)


@transaction.atomic
def subir_validar(request):
    acta, errores = validar_acta_json(request)

    if len(errores) > 0:
        return JsonResponse({'status': 'error', 'mensajes': errores}, status=400)

    return JsonResponse({'status': 'success', 'mensajes': ['El acta ha sido validada exitosamente.']})


@transaction.atomic
def subir_confirmar(request):
    acta, errores = validar_acta_json(request)
    # str_json = json.dumps(pre_acta)
    # print str_json
    # str_json = str_json.strip('\n')
    # real_acta = json.loads(str_json)
    # print real_acta
    if len(errores) > 0:
        return JsonResponse({'status': 'error', 'mensajes': errores}, status=400)

    errores = validar_cedulas_participantes(acta)

    if len(errores) == 0:
        uu = guardar_acta(acta)
        return JsonResponse(
            {'status': 'success', 'mensajes': [
                'El acta ha sido ingresada exitosamente. \n Su numero es: %s \n Recuerde guardarlo para posterior uso' % uu]})

    return JsonResponse({'status': 'error', 'mensajes': errores}, status=400)


def bajar_propuesta_docx(request, uuid):
    encuentro = ""
    try:
        encuentro = Encuentro.objects.filter(hash_search=uuid).first()
    except:
        return HttpResponseBadRequest()
    acta = encuentro.to_dict()

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


def enviar_pre_propuesta_docx(request):
    acta, errores = validar_acta_json(request)
    docx = generar_pre_propuesta_docx(acta)
    pre_propuesta_email(acta,acta['participante_organizador']['email'],docx)
    return JsonResponse(
            {'status': 'success', 'mensajes': [
                'El acta ha sido guardada exitosamente. Se le ha enviado un email con el borrador de la propuesta']})


def bajar_propuestas(request):
    return get_respuestas(request)


def bajar_datos(request, string):
    if string == 'Tipos_de_Encuentros':
        return get_tipos_encuentros(request)
    if string == 'Origenes':
        return get_origenes(request)
    if string == 'Lugares':
        return get_lugares(request)
    if string == 'Estamentos':
        return get_ocupaciones(request)
    if string == 'Encuentros':
        return get_encuentros(request)
    if string == 'Participantes':
        return get_participa(request)
    if string == 'Respuestas':
        return get_respuestas(request)

    return get_temas_encuentros(request)


def mostrar_acta(request):
    return render(request, 'mostrarActa.html')
