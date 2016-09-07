from django.db import models
from django.utils.encoding import smart_text
from django.utils.encoding import python_2_unicode_compatible
import uuid


class ConfiguracionEncuentro(models.Model):
    organizador = models.CharField(max_length=128)  ## esto tiene que ser u    n ID hacia el participante
    descripcion = models.CharField(max_length=1024)

    def __str__(self):
        return (u'<ConfiguracionEncuentro: organizador: {0}, descripcion: {1}, id{2}>'.format(self.organizador,
                                                                                              self.descripcion,
                                                                                              self.pk)).encode(
            'utf-8')

    def to_dict(self):
        return {
            'pk': self.pk,
            'organizador': self.organizador,
            'tipos': [i.to_dict() for i in self.tipoencuentro_set.all()],
            'lugares': [i.to_dict() for i in self.lugar_set.all()],
            'origenes': [i.to_dict() for i in self.origen_set.all()],
            'ocupaciones': [i.to_dict() for i in self.ocupacion_set.all()],
            'temas': [i.to_dict() for i in self.tema_set.all().order_by('orden')]
        }


class Lugar(models.Model):
    configuracion_encuentro = models.ForeignKey('ConfiguracionEncuentro', \
                                                on_delete=models.CASCADE)
    lugar = models.CharField(max_length=128)

    def __str__(self):
        return (
            (u'<Lugar: {0}, lugar: {1}>'.format(self.pk,
                                                self.lugar))).encode(
            'utf-8')

    def to_dict(self):
        return {
            'pk': self.pk,
            'nombre': self.lugar
        }


class Tema(models.Model):
    configuracion_encuentro = models.ForeignKey('ConfiguracionEncuentro', \
                                                on_delete=models.CASCADE)
    tema = models.CharField(max_length=128)
    contexto = models.TextField(blank=True, null=True)
    orden = models.IntegerField(default=1)

    def __str__(self):
        return (u'Tema id: {0} \nNombre: {1}'.format(self.pk, self.tema)).encode('utf-8')

    def to_dict(self):
        return {
            'pk': self.pk,
            'titulo': self.tema,
            'contextualizacion': self.contexto,
            'items': [i.to_dict() for i in self.itemtema_set.all()]
        }


class TipoEncuentro(models.Model):
    configuracion_encuentro = models.ForeignKey('ConfiguracionEncuentro', \
                                                on_delete=models.CASCADE)
    tipo = models.CharField(max_length=128)

    def __str__(self):
        return (u'Tipo Encuentro id: {0} \nNombre: {1}'.format(self.pk, self.tipo)).encode('utf-8')

    def to_dict(self):
        return {
            'pk': self.pk,
            'nombre': self.tipo
        }


class Origen(models.Model):
    configuracion_encuentro = models.ForeignKey('ConfiguracionEncuentro', \
                                                on_delete=models.CASCADE)
    origen = models.CharField(max_length=128)

    def __str__(self):
        return (u'Origen: {0} \nOrigen: {1}'.format(self.pk, self.origen)).encode(
            'utf-8')

    def to_dict(self):
        return {
            'pk': self.pk,
            'nombre': self.origen
        }


class Ocupacion(models.Model):
    configuracion_encuentro = models.ForeignKey('ConfiguracionEncuentro', \
                                                on_delete=models.CASCADE)
    ocupacion = models.CharField(max_length=128)

    def to_dict(self):
        return {
            'pk': self.pk,
            'nombre': self.ocupacion
        }

    def __str__(self):
        return (u'Ocupacion: {0} \nOcupacion: {1}'.format(self.pk,
                                                          self.ocupacion)).encode('utf-8')


class ItemTema(models.Model):
    tema = models.ForeignKey('Tema')
    pregunta = models.TextField(blank=True, null=True)
    pregunta_propuesta = models.TextField(blank=True, null=True)

    def __str__(self):
        return (u'<ItemTema: tema {0}>'.format(self.tema_id, self.pregunta, self.pregunta_propuesta)).encode('utf-8')

    def to_dict(self):
        return {
            'pk': self.pk,
            'pregunta': self.pregunta,
            'pregunta_propuesta': self.pregunta_propuesta
        }


class Encuentro(models.Model):
    configuracion_encuentro = models.ForeignKey('ConfiguracionEncuentro')
    tipo_encuentro = models.ForeignKey('TipoEncuentro')
    lugar = models.ForeignKey('Lugar')
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()
    encargado = models.ForeignKey('Participante')
    complemento = models.TextField(blank=True, null=True)
    hash_search = models.UUIDField(default=uuid.uuid1().hex)

    def __str__(self):
        return str({
            'pk': self.pk,
            'tipo_encuentro': self.tipo_encuentro.tipo,
            'lugar': self.lugar.lugar,
            'fecha_inicio': self.fecha_inicio,
            'hash': self.hash_search,
            'fecha_termino': self.fecha_termino,
            'encargado_id': self.encargado.pk,
             'complemento': self.complemento,
            'participantes': [i.to_dict() for i in self.participa_set.all()],
            'respuestas': [i.to_dict() for i in self.respuesta_set.all()]
        })

    def to_dict(self):
        return {
            'pk': self.pk,
            'tipo_encuentro': self.tipo_encuentro.tipo,
            'lugar': self.lugar.lugar,
            'fecha_inicio': self.fecha_inicio,
            'hash': self.hash_search,
            'fecha_termino': self.fecha_termino,
            'encargado_id': self.encargado.pk,
            'complemento': self.complemento,
            'participantes': [i.to_dict() for i in self.participa_set.all()],
            'respuestas': [i.to_dict() for i in self.respuesta_set.all()]
        }


class Respuesta(models.Model):
    CATEGORIA_OPCIONES = (
        {u'de_acuerdo', 2},
        {u'mayoria_de_acuerdo', 1},
        {u'desacuerdo', 0},
        {u'mayoria_desacuerdo', -1},
        {u'desacuerdo', -2},
    )
    item_tema = models.ForeignKey('ItemTema')
    encuentro = models.ForeignKey('Encuentro')
    categoria = models.IntegerField(choices=CATEGORIA_OPCIONES)
    fundamento = models.TextField(blank=True, null=True)
    propuesta = models.TextField(blank=True, null=True)

    def __str__(self):
        return (u'Item Tema: {0} \nEncuentro_id: {1} \nRespuesta: {2}'.format(self.item_tema, self.encuentro_id,
                                                                           self.fundamento[:125] + "...")).encode(
            'utf-8')

    def to_dict(self):
        item = self.item_tema
        tema = item.tema
        return {
            'pk': self.pk,
            'encuentro_id': self.encuentro_id,
            'tema': tema.tema,
            'pregunta': item.pregunta,
            'categoria': self.categoria,
            'respuesta': self.fundamento,
            'pregunta_propuesta': item.pregunta_propuesta,
            'propuesta': self.propuesta
        }


class Participante(models.Model):
    rut = models.CharField(max_length=11)
    nombre = models.CharField(max_length=128)
    apellido = models.CharField(max_length=128)
    correo = models.EmailField(max_length=128)
    numero_de_carnet = models.CharField(max_length=128)

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'apellido': self.apellido,
            'correo': self.correo
        }

    def __str__(self):
        return (u'Rut: {0} \nNombre: {1} \nApellido: {2}'.format(self.rut, self.nombre, self.apellido)).encode('utf-8')


class Participa(models.Model):
    participante = models.ForeignKey('Participante')
    encuentro = models.ForeignKey('Encuentro')
    ocupacion = models.ForeignKey('Ocupacion')
    origen = models.ForeignKey('Origen')

    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        return {
            'pk': self.pk,
            'encuentro_id': self.encuentro.pk,
            'ocupacion': self.ocupacion.ocupacion,
            'origen': self.origen.origen,
        }
