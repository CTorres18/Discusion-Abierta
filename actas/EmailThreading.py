# -*- coding: utf-8 -*-
import threading
from django.core.mail import send_mail, EmailMessage

__author__ = 'Nicolas'

class EmailThreadPropuesta(threading.Thread):
    def __init__(self, acta, ID):
        self.acta = acta
        self.ID = ID
        threading.Thread.__init__(self)

    def run(self):
        subject = "Participación en La Chile Piensa la Reforma"
        message = "Estimad@: \n Su Propuesta ha sido guardada en nuestro sistema, el código indentificador de su propuesta es {0} \n Puede recuperar su acta en la pagina web https://discusionabierta.dcc.uchile.cl/actas/bajarpropuestadocx/{0} .\n\n Este correo ha sido enviado automáticamente por el sistema de Discusión Abierta.\n Favor no responder.\n La Chile piensa la reforma: http://www.uchile.cl/discusion-reforma\n Dudas a +562 29780494 \n discusionreforma@uchile.cl\n Contacto equipo creador de la plataforma Discusión Abierta: \n contactodiscusionabierta@gmail.com".format(
            self.ID)
        from_email = "propuestas@dcc.uchile.cl"
        recipient_list = []
        for recipient in self.acta['participantes']:
            recipient_list.append(str(recipient['email']))
        encargado = self.acta['participante_organizador']
        recipient_list.append(str(encargado['email']))
        mensaje_html = None
        send_mail(subject, message, from_email, recipient_list, fail_silently=False, html_message=mensaje_html)

class EmailThreadPropuestaCIRES(threading.Thread):
    def __init__(self, acta, ID):
        self.acta = acta
        self.ID = ID
        threading.Thread.__init__(self)

    def run(self):
        subject = "Participación en La Chile Piensa la Reforma"
        message = "Estimad@: \n Se ha registrado una nueva propuesta cuyo identificador es {0} \n Puede descargar la propuesta en el siguiente link https://discusionabierta.dcc.uchile.cl/actas/bajarpropuestadocx/{0} .\n\n Este correo ha sido enviado automáticamente por el sistema de Discusión Abierta.\n Favor no responder.\n La Chile piensa la reforma: http://www.uchile.cl/discusion-reforma\n Dudas a +562 29780494 \n discusionreforma@uchile.cl\n Contacto equipo creador de la plataforma Discusión Abierta: \n contactodiscusionabierta@gmail.com".format(
            self.ID)
        from_email = "propuestas@dcc.uchile.cl"
        recipient_list = ['discusionreforma@uchile.cl']
        mensaje_html = None
        send_mail(subject, message, from_email, recipient_list, fail_silently=False, html_message=mensaje_html)


class EmailThreadPrePropuesta(threading.Thread):
    def __init__(self, encargado_email, file):
        self.encargado_email = encargado_email
        self.file = file
        threading.Thread.__init__(self)

    def run(self):
        subject = "Participación en La Chile Piensa la Reforma"
        message = "Estimad@:\n Su propuesta ha sido guarda exitosamente, pero solo en su computador, ahora puede apagar su computadora traquilamente y retomar su trabajo más tarde. Para ello, diríjase a la página de Discusión Abierta (https://discusionabierta.dcc.uchile.cl) y podrá seguir editando su propuesta. Una vez completada la edición, ésta podrá ser enviada para ser procesada a través del paso 4. Esto se hace presionando el botón 'Subir Propuesta' en la pestaña del mismo nombre.\n\n Una vez subida la propuesta, se le enviará un correo a los participantes de dicho encuentro, indicando el código identificador, con el cual puede revisar y verificar que efectivamente está almacenada en el sistema desde el menú 'Buscar mi propuesta'. Una vez enviada la propuesta, ésta ya no podrá ser modificada.\n\n Este correo ha sido enviado automáticamente por el sistema de Discusión Abierta. Favor no responder.\n\n Ante cualquier consulta escribir a: discusionreforma@uchile.cl\n\n Se despide atentamente Equipo de la plataforma Discusión Abierta"
        email = "propuestas@dcc.uchile.cl"
        email = EmailMessage(subject=subject, body=message, to=[self.encargado_email], from_email=email)
        #email.attach('pre_propuesta.docx', self.file.getvalue(),"application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        email.send()


def send_threaded_propuesta_mail(acta, ID):
    EmailThreadPropuesta(acta, ID).start()
    EmailThreadPropuestaCIRES(acta, ID).start()


def send_threaded_pre_propuesta_mail(acta, ID):
    EmailThreadPrePropuesta(acta, ID).start()
