from django.db import models
from django.utils.encoding import python_2_unicode_compatible

class ConfiguracionEncuentro(models.Model):
    organizador = models.CharField(max_length = 128)
    descripcion = models.CharField(max_length = 1024)

    @python_2_unicode_compatible
    def __str__(self):
        return 'Organizador: {0 : s} \nDescripcion: {1 : s}'.\
                    format(self.organizador, self.descripcion)

class Lugar(models.Model):
    configuracion_encuentro = models.ForeignKey('ConfiguracionEncuentro',  \
                                                on_delete = models.CASCADE)
    lugar = models.CharField(max_length = 128)

    @python_2_unicode_compatible
    def __str__(self):
        return 'Configuracion Encuentro: {0 : d} \nLugar: {1 : s}'.\
                    format(self.configuracion_encuentro, self.lugar)

class Tema(models.Model):
    configuracion_encuentro = models.ForeignKey('ConfiguracionEncuentro',  \
                                                on_delete = models.CASCADE)
    tema = models.CharField(max_length = 128)
    contexto = models.CharField(max_length = 1474560)

    @python_2_unicode_compatible
    def __str__(self):
        return 'Configuracion Encuentro: {0 : d} \nTema: {1 : s}'.\
                    format(self.configuracion_encuentro, self.tema)


class TipoEncuentro(models.Model):
    configuracion_encuentro = models.ForeignKey('ConfiguracionEncuentro', \
                                                on_delete = models.CASCADE)
    tipo = models.CharField(max_length = 128)

    @python_2_unicode_compatible
    def __str__(self):
        return 'Configuracion Encuentro: {0 : d} \nTipo Encuentro: {1 : s}'.\
                    format(self.configuracion_encuentro, self.tipo)


class Origen(models.Model):
    configuracion_encuentro = models.ForeignKey('ConfiguracionEncuentro', \
                                                on_delete = models.CASCADE)
    origen = models.CharField(max_length = 128)

    @python_2_unicode_compatible
    def __str__(self):
        return 'Configuracion Encuentro: {0 : d} \nOrigen: {1 : s}'.\
                    format(self.configuracion_encuentro, self.origen)


class Ocupacion(models.Model):
    configuracion_encuentro = models.ForeignKey('ConfiguracionEncuentro', \
                                                on_delete = models.CASCADE)
    ocupacion = models.CharField(max_length = 128)

    @python_2_unicode_compatible
    def __str__(self):
        return 'Configuracion Encuentro: {0 : d} \nOcupación: {1 : s}'.\
                    format(self.configuracion_encuentro, self.ocupacion)

class ItemTema(models.Model):
    tema_id = models.ForeignKey('Tema', on_delete = models.CASCADE)
    pregunta = models.CharField(max_length = 1024)
    pregunta_propuesta =models.CharField(max_length = 1024)

    @python_2_unicode_compatible
    def __str__(self):
        return 'Tema {0 : d} \nTipo: {1 : d} \nPregunta: {2 : s}'.\
                    format(self.tema_id, self.tipo, self.pregunta)


class Encuentro(models.Model):
    tipo_encuentro = models.ForeignKey('TipoEncuentro', on_delete = models.CASCADE)
    lugar = models.ForeignKey('Lugar', on_delete = models.CASCADE)
    fecha = models.DateField()
    rut_encargado = models.CharField(max_length = 11)

    @python_2_unicode_compatible
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
    respuesta = models.CharField(1024)
    propuesta = models.CharField(1024)


    @python_2_unicode_compatible
    def __str__(self):
        return 'Item Tema: {0 : d} \nEncuentro: {1 : d} \nRespuesta: {2 : s}'.\
                    format(self.item_tema, self.encuentro, self.respuesta[:125] + "...")


class Participante(models.Model):
    rut = models.CharField(max_length = 11)
    nombre = models.CharField(max_length = 128)
    apellido = models.CharField(max_length = 128)
    correo = models.EmaiField(max_length = 128)
    numero_de_carnet = models.CharField(max_length = 128)

    @python_2_unicode_compatible
    def __str__(self):
        return 'Rut: {0 : s} \nNombre: {1 : s} \nApellido: {2 : s}'.\
                    format(self.rut, self.nombre, self.apellido)



