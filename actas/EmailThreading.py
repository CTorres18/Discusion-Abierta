# -*- coding: utf-8 -*-
import threading
from django.core.mail import send_mail

__author__ = 'Nicolas'


class EmailThread(threading.Thread):
    def __init__(self, acta, ID):
        self.acta = acta
        self.ID = ID
        threading.Thread.__init__(self)

    def run(self):
        subject = "Participación en Discusión Abierta UChile"
        message = "Estimad@: \n La ID de su propuesta es {0} \n Puede recuperar su acta en la pagina web https://discusionabierta.dcc.uchile.cl/actas/bajarpropuestadocx/{0} .\n Este correo ha sido enviado automáticamente por el sistema de Discusión Abierta.\n Favor no responder.\n Para contactarse con el equipo tras esta plataforma comuníquese con Pablo Duarte:\npabduarte@uchile.cl\nSecretario Ejecutivo\nConsejo de Evaluación\nUniversidad de Chile\nFono: +56 229781148\nwww.uchile.cl/ConsejoEvaluacion.".format(
            self.ID)
        from_email = "propuestas@dcc.uchile.cl"
        recipient_list = []
        for recipient in self.acta['participantes']:
            recipient_list.append(str(recipient['email']))
        encargado = self.acta['participante_organizador']
        recipient_list.append(str(encargado['email']))
        mensaje_html = None
        send_mail(subject, message, from_email, recipient_list, fail_silently=False, html_message=mensaje_html)


def send_threaded_mail(acta, ID):
    EmailThread(acta, ID).start()
