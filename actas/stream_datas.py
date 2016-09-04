from actas.models import Encuentro, Participante,Participa

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
    print participan
    for p in participan:
        print p
    rows = ([str(participa.ocupacion.ocupacion),str(participa.origen.origen)] for participa in participan)
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="participantes.csv"'
    return response
