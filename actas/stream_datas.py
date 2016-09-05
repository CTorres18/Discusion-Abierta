from itertools import chain
from actas.models import Encuentro, Participante, Participa, Respuesta, Tema, ItemTema, Origen, Lugar, TipoEncuentro

__author__ = 'Nicolas'
import csv
from django.http import StreamingHttpResponse


class Echo(object):
    """An object that implements just the write method of the file-like
    interface.
    """

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def get_participantes_stream(request):
    """A view that streams a large CSV file."""
    # Generate a sequence of rows. The range is based on the maximum number of
    # rows that can be handled by a single sheet in most spreadsheet
    # applications.
    participan = Participa.objects.all()
    rows = ([participa.encuentro_id, participa.ocupacion_id, participa.origen_id] for participa in
            participan)
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="participantes.csv"'
    return response


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
             resp.fundamento, resp.propuesta] for resp in respuestas)

    def column_name_generator():
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
        return ([origen.pk, origen.origen] for origen in origenes)

    def column_name_generator():
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
        return ([lugar.pk, lugar.origen] for lugar in lugares)

    def column_name_generator():
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
        [encuentro.pk, encuentro.tipo_encuentro_id, encuentro.lugar_id, encuentro.fecha_inicio, encuentro.fecha_termino]
        for encuentro in encuentros)

    def column_name_generator():
        yield ("idEncuentro", "idTipoEncuentro","idLugar","fecha_inicio","fecha_termino")

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
        [tipo.pk, tipo.tipo]
        for tipo in tipos)

    def column_name_generator():
        yield ("idTipoEncuentro", "nombreTipo")

    rows = chain(column_name_generator(), tipos_generator(tipos_all))
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="encuentros.csv"'
    return response
