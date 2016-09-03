from django.db import models
from django.utils.encoding import python_2_unicode_compatible

class ConfiguracionEncuentro(models.Model):
    organizador = models.CharField(max_length = 128) ## esto tiene que ser u    n ID hacia el participante
    descripcion = models.CharField(max_length = 1024)

    def __repr__(self):
        return '<ConfiguracionEncuentro: organizador: {0}, descripcion: {1}>'.format(self.organizador, self.descripcion)
    def to_dict(self):
        return {
            'pk': self.pk,
            'organizador': self.tema,
            'tipos':  [i.to_dict() for i in self.tipoencuentro_set.all()],
            'lugares': [i.to_dict() for i in self.lugar_set.all()],
            'origenes' : [i.to_dict() for i in self.origen_set.all()],
            'ocupaciones' : [i.to_dict() for i in self.ocupacion_set.all()],
            'temas': [i.to_dict() for i in self.itema_set.all()]
        }


class Lugar(models.Model):
    configuracion_encuentro = models.ForeignKey('ConfiguracionEncuentro',  \
                                                on_delete = models.CASCADE)
    lugar = models.CharField(max_length = 128)

    def __str__(self):
        return '<Lugar: configuracion_encuentro: {0}, lugar: {1}>'.format(self.configuracion_encuentro, self.lugar)

class Tema(models.Model):
    configuracion_encuentro = models.ForeignKey('ConfiguracionEncuentro',  \
                                                on_delete = models.CASCADE)
    tema = models.CharField(max_length = 128)
    contexto = models.TextField(blank=True, null=True)
    def __str__(self):
        return '<Tema: encuentro: {0}, tema: {1}, contexto: {2}>'.format(self.configuracion_encuentro, self.tema,self.contexto)
    def to_dict(self):
        return {
            'pk': self.pk,
            'tema': self.tema,
            'items': [i.to_dict() for i in self.itemtema_set.all()]
        }


class TipoEncuentro(models.Model):
    configuracion_encuentro = models.ForeignKey('ConfiguracionEncuentro', \
                                                on_delete = models.CASCADE)
    tipo = models.CharField(max_length = 128)

    def __str__(self):
        return 'Configuracion Encuentro: {0 : d} \nTipo Encuentro: {1 : s}'.\
                    format(self.configuracion_encuentro, self.tipo)


class Origen(models.Model):
    configuracion_encuentro = models.ForeignKey('ConfiguracionEncuentro', \
                                                on_delete = models.CASCADE)
    origen = models.CharField(max_length = 128)

    def __str__(self):
        return 'Configuracion Encuentro: {0 : d} \nOrigen: {1 : s}'.\
                    format(self.configuracion_encuentro, self.origen)


class Ocupacion(models.Model):
    configuracion_encuentro = models.ForeignKey('ConfiguracionEncuentro', \
                                                on_delete = models.CASCADE)
    ocupacion = models.CharField(max_length = 128)

    def __str__(self):
        return 'Configuracion Encuentro: {0 : d} \nOcupacion: {1 : s}'.\
                    format(self.configuracion_encuentro, self.ocupacion)

class ItemTema(models.Model):
    tema = models.ForeignKey('Tema', on_delete = models.CASCADE)
    pregunta = models.TextField(blank=True, null=True)
    pregunta_propuesta =models.TextField(blank=True, null=True)

    def __str__(self):
        return '<ItemTema: tema {0}, tipo: {1}, pregunta: {2}>'.\
                    format(self.tema_id, self.tipo, self.pregunta)
    def to_dict(self):
        return {
            'pk': self.pk,
            'pregunta': self.pregunta,
            'pregunta_propuesta': self.pregunta_propuesta
        }


class Encuentro(models.Model):
    tipo_encuentro = models.ForeignKey('TipoEncuentro', on_delete = models.CASCADE)
    lugar = models.ForeignKey('Lugar', on_delete = models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()
    rut_encargado = models.CharField(max_length = 11)

    def __str__(self):
        return 'Tipo Encuentro: {0 : d} \nLugar: {1 : d} \n Encargado: {2 : s}'.\
                    format(self.tipo_encuentro, self.lugar, self.rut_encargado)

class Respuesta(models.Model):

    CATEGORIA_OPCIONES = (
        ('Acuerdo', 1),
        ('Acuerdo parcial', 0),
        ('Desacuerdo', -1),
    )
    item_tema = models.ForeignKey('ItemTema', on_delete = models.CASCADE)
    encuentro = models.ForeignKey('Encuentro', on_delete = models.CASCADE)
    categoria = models.IntegerField(choices=CATEGORIA_OPCIONES)
    fundamento = models.TextField(blank=True, null=True)
    propuesta = models.TextField(blank=True, null=True)


    def __str__(self):
        return 'Item Tema: {0 : d} \nEncuentro: {1 : d} \nRespuesta: {2 : s}'.\
                    format(self.item_tema, self.encuentro, self.respuesta[:125] + "...")


class Participante(models.Model):
    rut = models.CharField(max_length = 11)
    nombre = models.CharField(max_length = 128)
    apellido = models.CharField(max_length = 128)
    correo = models.EmailField(max_length = 128)
    numero_de_carnet = models.CharField(max_length = 128)

    def __str__(self):
        return 'Rut: {0 : s} \nNombre: {1 : s} \nApellido: {2 : s}'.\
                    format(self.rut, self.nombre, self.apellido)



