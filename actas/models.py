from django.db import models
from django.utils.encoding import python_2_unicode_compatible


class ConfiguracionEncuentro(models.Model):
    organizador = models.CharField(max_length=128)  ## esto tiene que ser u    n ID hacia el participante
    descripcion = models.CharField(max_length=1024)

    def __str__(self):
        return (u'<ConfiguracionEncuentro: organizador: {0}, descripcion: {1}>'.format(self.organizador, self.descripcion)).encode('utf-8')

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
        return (u'<Lugar: configuracion_encuentro: {0}, lugar: {1}>'.format(self.configuracion_encuentro, self.lugar)).encode('utf-8')

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
        return (u'<Tema: encuentro: {0}, tema: {1}, contexto: {2}>'.format(self.configuracion_encuentro, self.tema,
                                                                         self.contexto)).encode('utf-8')

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
        return (u'Configuracion Encuentro: {0},Tipo Encuentro: {1}'.format(self.configuracion_encuentro, self.tipo)).encode('utf-8')

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
        return (u'Configuracion Encuentro: {0} \nOrigen: {1}'.format(self.configuracion_encuentro, self.origen)).encode('utf-8')

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
        return (u'Configuracion Encuentro: {0} \nOcupacion: {1}'.format(self.configuracion_encuentro,
                                                                              self.ocupacion)).encode('utf-8')


class ItemTema(models.Model):
    tema = models.ForeignKey('Tema', on_delete=models.CASCADE)
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
    tipo_encuentro = models.ForeignKey('TipoEncuentro', on_delete=models.CASCADE)
    lugar = models.ForeignKey('Lugar', on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()
    rut_encargado = models.CharField(max_length=11)

    def __str__(self):
        return (u'Tipo Encuentro: {0} \nLugar: {1} \n Encargado: {2}'.format(self.tipo_encuentro, self.lugar,
                                                                                       self.rut_encargado)).encode('utf-8')


class Respuesta(models.Model):
    CATEGORIA_OPCIONES = (
        {u'de_acuerdo',2},
        {u'mayoria_de_acuerdo',1},
        {u'desacuerdo',0},
        {u'mayoria_desacuerdo',-1},
        {u'desacuerdo',-2},
    )
    item_tema = models.ForeignKey('ItemTema', on_delete=models.CASCADE)
    encuentro = models.ForeignKey('Encuentro', on_delete=models.CASCADE)
    categoria = models.IntegerField(choices=CATEGORIA_OPCIONES)
    fundamento = models.TextField(blank=True, null=True)
    propuesta = models.TextField(blank=True, null=True)

    def __str__(self):
        return (u'Item Tema: {0} \nEncuentro: {1} \nRespuesta: {2}'.format(self.item_tema, self.encuentro,
                                                                                     self.respuesta[:125] + "...")).encode('utf-8')


class Participante(models.Model):
    rut = models.CharField(max_length=11)
    nombre = models.CharField(max_length=128)
    apellido = models.CharField(max_length=128)
    correo = models.EmailField(max_length=128)
    numero_de_carnet = models.CharField(max_length=128)

    def __str__(self):
        return (u'Rut: {0} \nNombre: {1} \nApellido: {2}'.format(self.rut, self.nombre, self.apellido)).encode('utf-8')
