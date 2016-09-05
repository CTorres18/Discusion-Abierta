# -*- coding: utf-8 -*-
import json
from itertools import cycle
import re

from django.conf import settings
from models import Tema, ItemTema, Origen, Ocupacion, Encuentro, Participante, ConfiguracionEncuentro, Lugar, Participa
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils import timezone
from pyquery import PyQuery as pq
import requests
from stream_datas import get_participantes_stream

# from .models import Comuna, Acta, Item, ActaRespuestaItem


REGEX_RUT = re.compile(r'([0-9]+)\-([0-9K])', re.IGNORECASE)
RUT_VERIFICACION_URL = 'https://portal.sidiv.registrocivil.cl/usuarios-portal/pages/DocumentRequestStatus.xhtml?RUN={0:s}&type=CEDULA&serial={1:s}'


# https://gist.github.com/rbonvall/464824
def _digito_verificador(rut):
    reversed_digits = map(int, reversed(str(rut)))
    factors = cycle(range(2, 8))
    s = sum(d * f for d, f in zip(reversed_digits, factors))
    return (-s) % 11


def verificar_rut(rut_con_dv):
    if type(rut_con_dv) not in [str, unicode] \
            or len(rut_con_dv) == 0 \
            or REGEX_RUT.match(rut_con_dv) is None:
        return False

    rut_con_dv = rut_con_dv.upper()

    rut = rut_con_dv[:-2]
    dv = rut_con_dv[-1]

    if dv == 'K':
        dv = 10
    dv = int(dv)

    digito = _digito_verificador(rut)

    return digito == dv


def _get_html_verificar_cedula(rut_con_dv, serie):
    r = requests.get(
        RUT_VERIFICACION_URL.format(rut_con_dv, serie),
        verify=False  # Registro Civil pls
    )

    if r.status_code != 200:
        return None

    return r.content


def verificar_cedula(rut_con_dv, serie):
    result = []

    if type(rut_con_dv) not in [str, unicode] \
            or len(rut_con_dv) == 0 \
            or not verificar_rut(rut_con_dv):
        result.append('RUT inválido ({0})'.format(rut_con_dv) if rut_con_dv is not None and len(
            rut_con_dv) > 0 else 'RUT inválido')

    if type(serie) not in [str, unicode] or len(serie) == 0:
        result.append('Número de serie inválido para el RUT {0:s}'.format(rut_con_dv) if rut_con_dv is not None and len(
            rut_con_dv) > 0 else 'Número de serie inválido')

    if len(result) > 0:
        return result

    serie = serie.upper()

    html = _get_html_verificar_cedula(rut_con_dv, serie)

    if html is None:
        result.append('Validación de cédula no disponible.')
        return result

    html = html.replace(
        '<html xmlns="http://www.w3.org/1999/xhtml">',
        '<html>'
    )

    document = pq(html)

    verificacion_rut = document('form input#form\:run').val()
    verificacion_serie = document('form input#form\:docNumber').val()
    vigente = document('table#tableResult td.setWidthOfSecondColumn').text().upper() == 'VIGENTE'

    if rut_con_dv != verificacion_rut:
        result.append('RUT no coincide para el RUT {0:s}'.format(rut_con_dv))

    if serie != verificacion_serie:
        result.append('Número de serie no coincide para el rut {0:s}'.format(rut_con_dv))

    if not vigente:
        result.append('El documento de identidad no está vigente para el RUT {0:s}'.format(rut_con_dv))

    return result


def validar_datos_geograficos(acta):
    errores = []

    # comuna_seleccionada = acta.get('geo', {}).get('comuna')
    # provincia_seleccionada = acta.get('geo', {}).get('provincia')
    # region_seleccionada = acta.get('geo', {}).get('region')
    #
    # if type(region_seleccionada) != int:
    #     return ['Región inválida.']
    #
    # if type(provincia_seleccionada) != int:
    #     return ['Provincia inválida.']
    #
    # if type(comuna_seleccionada) != int:
    #     return ['Comuna inválida.']
    #
    # comunas = Comuna.objects.filter(pk=comuna_seleccionada)
    #
    # if len(comunas) != 1:
    #     errores.append('Comuna inválida.')
    # else:
    #     if comunas[0].provincia.pk != provincia_seleccionada:
    #         errores.append('Provincia no corresponde a la comuna.')
    #
    #     if comunas[0].provincia.region.pk != region_seleccionada:
    #         errores.append('Región no corresponde a la provincia.')

    return errores


def validar_origenes(acta):
    errores = []
    acta['participante_organizador']
    origenes = set([p['origen'] for p in acta['participantes']])
    origenes.update([acta['participante_organizador']['origen']])
    for origen in origenes:
        if not Origen.objects.filter(origen=origen).exists():
            errores.append('Existen orígenes inválidos.')
            return errores
    return errores


def validar_lugar(acta):
    errores = []
    configuracion_encuentro=ConfiguracionEncuentro.objects.get(pk=acta['pk'])
    if not Lugar.objects.filter(configuracion_encuentro=configuracion_encuentro, lugar=acta['lugar']).exists():
        errores.append('Lugar Inválido.')
    return errores


def validar_ocupaciones(acta):
    errores = []
    acta['participante_organizador']
    ocupaciones = set([p['ocupacion'] for p in acta['participantes']])
    ocupaciones.update([acta['participante_organizador']['ocupacion']])
    for ocupacion in ocupaciones:
        if not Ocupacion.objects.filter(ocupacion=ocupacion).exists():
            errores.append('Existen ocupaciones inválidos.')
            return errores
    return errores


def validar_temas(acta):
    errores = []
    for tema in acta['temas']:
        if not Tema.objects.filter(pk=tema['pk']).exists():
            errores.append('Error en la verificación del tema.')
            return errores
        errores += validar_items(tema['items'])
    return errores


def validar_items(items):
    errores = []
    for item in items:
        if 'categoria' in item:
            if not ItemTema.objects.filter(pk=item['pk']).exists():
                errores.append('Error en la verificación del tema.')
                break
    return errores


def validar_tipo_encuentro(acta):
    errores = []
    return errores


def validar_participantes(acta):
    errores = []
    obtener_config()

    participante_organizador = acta.get('participante_organizador', {})
    participantes = acta.get('participantes', [])
    config = obtener_config()

    # tienen que existir la cantidad de participantes aceptada
    if participante_organizador == {}:
        errores.append('Error en el formato del participante organizador.')

    if type(participantes) != list \
            or not (config['participantes_min'] <= len(participantes) <= config['participantes_max']):
        errores.append('Error en el formato de los participantes.')

    if len(errores) > 0:
        return errores

    errores += _validar_participante(participante_organizador, 0)
    for i, participante in enumerate(participantes):
        errores += _validar_participante(participante, i + 1)

    if len(errores) > 0:
        return errores

    ruts_participantes = [p['rut'] for p in participantes]
    ruts_participantes.append(participante_organizador['rut'])

    # validar emailstry:
    try:
        validate_email(participante_organizador['email'])
        for participante in participantes:
            validate_email(participante['email'])
    except ValidationError as e:
        errores.append('Existen emails inválidos.')

    # Ruts diferentes
    ruts = set(ruts_participantes)
    if not len(ruts) <= len(ruts_participantes):
        return ['Existen RUTs repetidos.']

    for rut in ruts:
        if not verificar_rut(rut):
            errores.append('Existen RUTs inválidos.')
            return errores

    if len(errores) > 0:
        return errores

    # Verificar que los participantes no hayan enviado un acta antes
    participantes_en_db = Participante.objects.filter(rut__in=list(ruts))

    if len(participantes_en_db) > 0:
        for participante in participantes_en_db:
            errores.append('El RUT {0:s} ya participó del proceso.'.format(participante.rut))

    errores += verificar_cedula(participante_organizador['rut'], participante_organizador['serie_cedula'])
    return errores


def _validar_participante(participante, pos):
    errores = []
    error = False
    str_error = 'Falta '

    if not 'nombre' in participante:
        str_error += 'nombre, '
        error = True

    if not 'apellido' in participante:
        str_error += 'apellido, '
        error = True

    if not 'rut' in participante:
        str_error += 'RUT, '
        error = True

    if not 'email' in participante:
        str_error += 'email, '
        error = True

    if not 'ocupacion' in participante:
        str_error += 'ocupacion, '
        error = True

    if not 'origen' in participante:
        str_error += 'origen, '
        error = True

    str_error = str_error[:-2]
    if pos == 0:
        str_error += ' del participante organizador.'
    else:
        str_error += ' del participante {0:d}.'.format(pos)
    # if type(participante) != dict:
    #     errores.append('Datos del participante {0:d} inválidos.'.format(pos))
    #     return errores
    #
    # if not verificar_rut(participante.get('rut')):
    #     errores.append('RUT del participante {0:d} es inválido.'.format(pos))
    #     return errores
    #
    # nombre = participante.get('nombre')
    # apellido = participante.get('apellido')
    #
    # if type(nombre) not in [str, unicode] or len(nombre) < 2:
    #     errores.append('Nombre del participante {0:d} es inválido.'.format(pos))
    #
    # if type(apellido) not in [str, unicode] or len(apellido) < 2:
    #     errores.append('Apellido del participante {0:d} es inválido.'.format(pos))
    if error:
        errores.append(str_error)
    return errores


def validar_cedulas_participantes(acta):
    errores = []
    #
    # participantes = acta.get('participantes', [])
    #
    # for participante in participantes:
    #     errores += verificar_cedula(participante.get('rut'), participante.get('serie_cedula'))

    return errores


# def validar_items(acta):
# errores = []

# items_por_responder = map(lambda i: i.pk, Item.objects.all())
#
# for group in acta['itemsGroups']:
#     for i, item in enumerate(group['items']):
#         acta_item = Item.objects.filter(pk=item.get('pk'))
#
#         if len(acta_item) != 1 or acta_item[0].nombre != item.get('nombre'):
#             errores.append(
#                 'Existen errores de validación en ítem {0:d}.'.format(
#                     item['pk']
#                 )
#             )
#             return errores
#
#         if item.get('categoria') not in ['-1', '0', '1']:
#             errores.append(
#                 'No se ha seleccionado la categoría del ítem {0:d}.'.format(
#                     item['pk']
#                 )
#             )
#             return errores
#
#         items_por_responder.remove(int(item['pk']))
#
# if len(items_por_responder) > 0:
#     errores.append('No se han respondido todos los items del acta.')

# return errores


def insertar_participantes(participantes, datos_acta,encuentro):
    configuracion_encuentro=ConfiguracionEncuentro.objects.get(pk=datos_acta['pk'])

    for participante in participantes:

        #origen valido
        origen = Origen.objects.filter(configuracion_encuentro=configuracion_encuentro, origen=participante['origen'])
        origen_pk = -1
        if origen.exists():
            origen_pk = origen[0].pk
        else:
            return ['Origen inválido.']

        #ocupacion valido
        ocupacion = Ocupacion.objects.filter(configuracion_encuentro=configuracion_encuentro, ocupacion=participante['ocupacion'])
        ocupacion_pk = -1
        if ocupacion.exists():
            ocupacion_pk = ocupacion[0].pk
        else:
            return ['Ocupación inválido.']

        #serie sedula para el organizador
        serie_cedula = ''
        if 'serie_cedula' in participante:
            serie_cedula = participante['serie_cedula']

        #guardar participante
        p_db = Participante(rut=participante['rut'], nombre=participante['nombre'], apellido=participante['apellido'],
                            correo=participante['email'], numero_de_carnet=serie_cedula)
        p_db.save()
        participa_encuentro= Participa(encuentro_id= encuentro.pk,
                                        participante_id=p_db.pk,
                                        ocupacion_id=ocupacion_pk,
                                        origen_id=origen_pk)
        participa_encuentro.save()


def guardar_acta(datos_acta):
    p_encargado = datos_acta['participante_organizador']
    encargado = Participante(rut=p_encargado['rut'], nombre=p_encargado['nombre'], apellido=p_encargado['apellido'],
                             correo=p_encargado['email'], numero_de_carnet=p_encargado['serie_cedula'])
    encargado.save()



    # obtener el pk del tipo
    tipo_pk = -1
    for tipo in datos_acta['tipos']:
        if tipo['nombre'] == datos_acta['tipo']:
            tipo_pk = tipo['pk']

    # obtener el pk del lugar
    lugar_pk = -1
    for lugar in datos_acta['lugares']:
        if lugar['nombre'] == datos_acta['lugar']:
            lugar_pk = lugar['pk']

    #guardar encuentro
    encuentro = Encuentro(  fecha_inicio='1990-01-01', fecha_termino='1990-01-01',
                            tipo_encuentro_id=tipo_pk, lugar_id=lugar_pk, encargado_id=encargado.pk,
                            configuracion_encuentro_id=datos_acta['pk'])

    encuentro.save()
    participantes = datos_acta['participantes']
    participantes.append(datos_acta['participante_organizador'])
    print participantes
    insertar_participantes(participantes, datos_acta,encuentro)
    # acta = Acta(
    #     comuna=Comuna.objects.get(pk=datos_acta['geo']['comuna']),
    #     memoria_historica=datos_acta.get('memoria'),
    #     fecha=timezone.now(),
    # )
    #
    # acta.save()
    #
    # for p in datos_acta['participantes']:
    #     acta.participantes.add(_crear_usuario(p))
    #
    # acta.save()
    #
    # for group in datos_acta['itemsGroups']:
    #     for i in group['items']:
    #         item = Item.objects.get(pk=i['pk'])
    #         acta_item = ActaRespuestaItem(
    #             acta=acta,
    #             item=item,
    #             categoria=i['categoria'],
    #             fundamento=i.get('fundamento')
    #         )
    #         acta_item.save()


def enviar_email_a_participantes(acta):
    subject = "Participación en Discusión Abierta UChile"
    message = "Estimade: El contenido del acta es: bleh bleh bleh"
    from_email = "no-responder@discusionabierta.cl"
    recipient_list = []
    for recipient in acta.participantes:
        recipient_list.extend(str(recipient.mail))
    mensaje_html = None
    send_mail(subject, message, from_email, recipient_list, fail_silently=False, html_message=mensaje_html)


def validar_acta_json(request):
    if request.method != 'POST':
        return (None, 'Request inválido.',)

    acta = request.body.decode('utf-8')

    try:
        acta = json.loads(acta)
    except ValueError:
        return (None, 'Acta inválida.',)
    validation_functions = [validar_origenes, validar_lugar, validar_ocupaciones, validar_temas, validar_tipo_encuentro,
                            validar_participantes]
    for function in validation_functions:
        errores = function(acta)

        if len(errores) > 0:
            return (acta, errores,)

    return (acta, [],)


def get_participantes(request):
    return get_participantes_stream(request)


def obtener_config():
    config = {
        'participantes_min': 3,
        'participantes_max': 50,
        'encuentro': 20,

    }

    if hasattr(settings, 'DISCUSION_ABIERTA') and type(settings.DISCUSION_ABIERTA) == dict:
        config['participantes_min'] = int(
            settings.DISCUSION_ABIERTA.get('PARTICIPANTES_MIN', config['participantes_min'])
        )
        config['participantes_max'] = int(
            settings.DISCUSION_ABIERTA.get('PARTICIPANTES_MAX', config['participantes_max'])
        )

    return config


def _crear_usuario(datos_usuario):
    usuario = User(username=datos_usuario['rut'])
    usuario.first_name = datos_usuario['nombre']
    usuario.last_name = datos_usuario['apellido']
    usuario.save()
    return usuario
