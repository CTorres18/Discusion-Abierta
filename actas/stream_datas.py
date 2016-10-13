# coding=utf-8
from itertools import chain
from actas.models import Encuentro, Participante, Participa, Respuesta, Tema, ItemTema, Origen, Lugar, TipoEncuentro

__author__ = 'Nicolas'
import csv
from django.http import StreamingHttpResponse
from itertools import groupby, chain


class Echo(object):
    """An object that implements just the write method of the file-like
    interface.
    """

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


# def get_respuestas(request):
#     def generator1(respuestas):
#         return (
#         [respuesta.item_tema.pregunta.encode('utf-8'), respuesta.categoria, respuesta.fundamento.encode('utf-8'),
#          respuesta.item_tema.pregunta_propuesta.encode('utf-8'), respuesta.propuesta.encode('utf-8')] for respuesta
#         in respuestas)
#
#     def generator2():
#         yield ("Pregunta", "Categoria", "Fundamento", "Pregunta propuesta", "Propuesta")
#
#     respuestas = Respuesta.objects.all().order_by('item_tema_id')
#     rows = chain(generator2(), generator1(respuestas))
#     pseudo_buffer = Echo()
#     writer = csv.writer(pseudo_buffer)
#     response = StreamingHttpResponse((writer.writerow(row) for row in rows),
#                                      content_type="text/csv")
#     response['Content-Disposition'] = 'attachment; filename="respuestas.csv"'
#     return response



def get_respuestas(request):
    resp_all = Respuesta.objects.all().order_by('encuentro_id')
    items_all = ItemTema.objects.all()

    def respuestas_generator(respuestas, items):
        return (
            [resp.encuentro_id, items.filter(pk=resp.item_tema_id).first().tema_id, resp.item_tema_id, resp.categoria,
             resp.fundamento.encode('utf-8'), resp.propuesta.encode('utf-8')] for resp in respuestas)

    def column_name_generator():
        yield ("Respuestas", "")
        yield ("idEncuentro", "idTema", "idItem", "categoria", "fundamento", "propuesta")

    rows = chain(column_name_generator(), respuestas_generator(resp_all, items_all))
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="respuestas.csv"'
    return response


def get_origenes(request):
    origen_all = Origen.objects.all()

    def origen_generator(origenes):
        return ([origen.pk, origen.origen.encode('utf-8')] for origen in origenes)

    def column_name_generator():
        yield ("Organismos", "")
        yield ("idOrigen", "nombreOrigen")

    rows = chain(column_name_generator(), origen_generator(origen_all))
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="origenes.csv"'
    return response


def get_lugares(request):
    lugar_all = Lugar.objects.all()

    def lugar_generator(lugares):
        return ([lugar.pk, lugar.lugar.encode('utf-8')] for lugar in lugares)

    def column_name_generator():
        yield ("Lugares", "")
        yield ("idLugar", "nombreLugar")

    rows = chain(column_name_generator(), lugar_generator(lugar_all))
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="lugares.csv"'
    return response


def get_encuentros(request):
    encuentros_all = Encuentro.objects.all()

    def encuentros_generator(encuentros):
        return (
            [encuentro.pk, encuentro.tipo_encuentro.tipo, encuentro.lugar.lugar, encuentro.fecha_inicio,
             encuentro.fecha_termino, encuentro.complemento.encode('utf-8')]
            for encuentro in encuentros)

    def column_name_generator():
        yield ("Encuentros", "")
        yield ("idEncuentro", "TipoEncuentro", "idLugar", "fecha_inicio", "fecha_termino", "complemento")

    rows = chain(column_name_generator(), encuentros_generator(encuentros_all))
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="encuentros.csv"'
    return response


def get_tipos_encuentros(request):
    tipos_all = TipoEncuentro.objects.all()

    def tipos_generator(tipos):
        return (
            [tipo.pk, tipo.tipo.encode('utf-8')]
            for tipo in tipos)

    def column_name_generator():
        yield ("Tipos de Encuentro", "")
        yield ("idTipoEncuentro", "nombreTipo")

    rows = chain(column_name_generator(), tipos_generator(tipos_all))
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="tipo_encuentros.csv"'
    return response


def get_temas_encuentros(request):
    temas_all = Tema.objects.all()

    def temas_generator(temas):
        return (
            [tema.pk, tema.tema.encode('utf-8')]
            for tema in temas)

    def column_name_generator():
        yield ("Temas", "")
        yield ("idTipoEncuentro", "nombreTipo")

    rows = chain(column_name_generator(), temas_generator(temas_all))
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="temas.csv"'
    return response


def get_ocupaciones(request):
    ocupaciones_all = Encuentro.objects.all()

    def ocupaciones_generator(ocupaciones):
        return (
            [ocupacion.pk, ocupacion.ocupacion.encode('utf-8')]
            for ocupacion in ocupaciones)

    def column_name_generator():
        yield ("Estamentos", "")
        yield ("idOcupacion", "nombreOcupacion")

    rows = chain(column_name_generator(), ocupaciones_generator(ocupaciones_all))
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="ocupacion.csv"'
    return response


def get_propuestas_cires(request):
    resp_all = Respuesta.objects.all().order_by('encuentro_id')
    items_all = ItemTema.objects.all()

    def generate_users_info(respuesta):
        users = respuesta.encuentro.participa_set.all()
        origen_pre = list(chain.from_iterable([[user.origen_id for user in users],
                                               [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
                                                34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46]]))
        estamento_pre = list(chain.from_iterable([[user.ocupacion_id for user in users], [16, 17, 18, 19]]))
        origen_pre.sort()
        estamento_pre.sort()
        cantidad = len(users)
        origenes = [(len(list(group)) - 1) for key, group in groupby(origen_pre)]
        estamentos = [(len(list(group)) - 1) for key, group in groupby(estamento_pre)]
        return chain.from_iterable([[cantidad], estamentos, origenes])

    def respuestas_generator(respuestas, items):
        return (
            list(chain.from_iterable([[resp.encuentro_id], [resp.encuentro.tipo_encuentro.tipo],
                                      [items.filter(pk=resp.item_tema_id).first().tema_id], [resp.categoria],
                                      generate_users_info(resp),
                                      [resp.fundamento.encode('utf-8')], [resp.propuesta.encode('utf-8')]])) for resp in
            respuestas)

    def column_name_generator():
        yield (
            "Encuentro", "Tipo", "Tema", "Categoria", "Total Participantes", "Académica(o)",
            "Funcionaria(o)",
            "Estudiante",
            "Egresada(o)",
            "Facultad de Arquitectura y Urbanismo", "Facultad de Artes", "Facultad de Ciencias",
            "Facultad de Ciencias Agronómicas", "Facultad de Economía y Negocios",
            "Facultad de Ciencias Físicas y Matemáticas",
            "Facultad de Ciencias Forestales y de la Conservación de la Naturaleza",
            "Facultad de Ciencias Químicas y Farmacéuticas", "Facultad de Ciencias Sociales",
            "Facultad de Ciencias Veterinarias y Pecuarias", "Facultad de Derecho",
            "Facultad de Filosofía y Humanidades", "Facultad de Medicina", "Facultad de Odontología",
            "Instituto de Nutrición y Tecnología de los Alimentos", "Instituto de Estudios Internacionales",
            "Instituto de Asuntos Públicos", "Instituto de la Comunicación e Imagen",
            "Programa Académico de Bachillerato", "Hospital Clínico", "Rectoría", "Prorrectoría",
            "Vicerrectoría de Asuntos Académicos", "Vicerrectoría de Asuntos Económicos y Gestión Institucional",
            "Secretaría General", "Vicerrectoría de Investigación y Desarrollo", "Vicerrectoría de Extensión",
            "Vicerrectoría de Asuntos Estudiantiles y Comunitarios", "Centro de Extensión Artística y Cultural ",
            "Liceo Manuel de Salas", "Departamento de Evaluación Medición y Registro Educacional", "Fundamento",
            "Propuesta")

    rows = chain(column_name_generator(), respuestas_generator(resp_all, items_all))
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="propuestas.csv"'
    return response


def get_participa(request):
    participantes_all = Participa.objects.all()

    def participantes_generator(participantes):
        return (
            [participa.encuentro_id, participa.participante_id, participa.ocupacion_id, participa.origen_id]
            for participa in participantes)

    def column_name_generator():
        yield ("Participantes", "")
        yield ("idEncuentro", "idParticipante", "idOcupacion", "idOrigen")

    rows = chain(column_name_generator(), participantes_generator(participantes_all))
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="participantes.csv"'
    return response
