from itertools import chain
from actas.models import Encuentro, Participante, Participa, Respuesta

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
    rows = ([str(participa.ocupacion.ocupacion), str(participa.origen.origen)] for participa in participan)
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="participantes.csv"'
    return response


def get_respuestas(request):
    def generator1(respuestas):
        return ([respuesta.item_tema.pregunta.encode('utf-8'), respuesta.categoria, respuesta.fundamento.encode('utf-8'),
                 respuesta.item_tema.pregunta_propuesta.encode('utf-8'), respuesta.propuesta.encode('utf-8')] for respuesta
                in respuestas)


    def generator2():
        yield ("Pregunta", "Categoria", "Fundamento", "Pregunta propuesta", "Propuesta")
    respuestas = Respuesta.objects.all().order_by('item_tema_id')
    rows = chain(generator2(), generator1(respuestas))
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="respuestas.csv"'
    return response



