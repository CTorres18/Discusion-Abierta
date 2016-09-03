from actas.models import ConfiguracionEncuentro,Tema,ItemTema

__author__ = 'Nicolas'


from django.test import TestCase


class DatabaseToDictTests(TestCase):
    def database_to_dict_test(self):
        cfg1=ConfiguracionEncuentro(organizador="doge", descripcion="pene")
        cfg1.save()
        tema1=Tema(configuracion_encuentro_id=1, tema="caquita", contexto="dcc")
        tema1.save()
        item1_tema1=ItemTema(tema_id=1, pregunta="doge se la come?", pregunta_propuesta="풹travesada? 풹 dos manos?")
        item1_tema1.save()
        item2_tema1=ItemTema(tema_id=1, pregunta="hihose la come?", pregunta_propuesta="풹travesada? 풹 dos manos?")
        item2_tema1.save()
        print tema1