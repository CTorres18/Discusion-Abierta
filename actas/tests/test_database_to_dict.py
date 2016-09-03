# -*- coding: utf-8 -*-

import json

from actas.models import *
from django.test import TestCase

__author__ = 'Nicolas'



class DatabaseToDictTests(TestCase):
    def test_database_to_dict(self):
        expected_result = {
            "lugares": [
                {"lugar": u"fcfm","pk": 1}, {"lugar": u"piedragogico","pk": 2}
            ],
            "ocupaciones": [
                {"ocupacion": u"vagabundo", "pk": 1},
                {"ocupacion": u"academico", "pk": 2}
            ],
            "organizador": u"doge",
            "origenes": [
                {"origen": u"fcfm", "pk": 1},
                {"origen": u"piedragogico", "pk": 2}
            ],
            "pk": 1,
            "temas": [
                {
                    "items": [
                        {
                            "pk": 3,
                            "pregunta": u"doge2 se la come?",
                            "pregunta_propuesta": u"\u00bfatravesada2? \u00bfa dos manos2?"
                        }
                    ],
                    "pk": 2,
                    "tema": u"caquita2"
                },
                {
                    "items": [
                        {
                            "pk": 1,
                            "pregunta": u"doge se la come?",
                            "pregunta_propuesta": u"\u00bfatravesada? \u00bfa dos manos?"
                        },
                        {
                            "pk": 2,
                            "pregunta": u"hihose la come?",
                            "pregunta_propuesta": u"\u00bfatravesada? \u00bfa dos manos?"
                        }
                    ],
                    "pk": 1,
                    "tema": u"caquita"
                }
            ],
            "tipos": [
                {"pk": 1, "tipo": u"sensual"},
                {"pk": 2, "tipo": u"sepsi"}
            ]
        }
        cfg1=ConfiguracionEncuentro(organizador="doge", descripcion="pene")
        cfg1.save()
        tema1=Tema(
            configuracion_encuentro_id=cfg1.pk,
            tema="caquita",
            contexto="dcc",
            orden=2
        )
        tema1.save()
        item1_tema1=ItemTema(
            tema_id=tema1.pk,
            pregunta="doge se la come?", pregunta_propuesta=u"¿atravesada? ¿a dos manos?")
        item1_tema1.save()
        item2_tema1=ItemTema(
            tema_id=tema1.pk,
            pregunta="hihose la come?",
            pregunta_propuesta=u"¿atravesada? ¿a dos manos?"
        )
        item2_tema1.save()
        tema2=Tema(
            configuracion_encuentro_id=cfg1.pk,
            tema="caquita2",
            contexto="dcc2",
            orden=1
        )
        tema2.save()
        item2_tema2=ItemTema(
            tema_id=tema2.pk,
            pregunta="doge2 se la come?",
            pregunta_propuesta=u"¿atravesada2? ¿a dos manos2?"
        )
        item2_tema2.save()
        item2_tema12=ItemTema(
            tema_id=tema2.pk,
            pregunta="hihose la come2?",
            pregunta_propuesta=u"¿atravesada2? ¿a dos manos2?"
        )
        item2_tema2.save()
        tipo1 = TipoEncuentro(
            configuracion_encuentro_id=cfg1.pk,
            tipo="sensual"
        )
        tipo1.save()
        tipo2 = TipoEncuentro(
            configuracion_encuentro_id=cfg1.pk,
            tipo="sepsi"
        )
        tipo2.save()
        origen1 = Origen(
            configuracion_encuentro_id=cfg1.pk,
            origen="fcfm"
        )
        origen1.save()
        origen2 = Origen(
            configuracion_encuentro_id=cfg1.pk, origen="piedragogico"
        )
        origen2.save()
        lugar1 = Lugar(
            configuracion_encuentro_id=cfg1.pk, lugar="fcfm"
        )
        lugar1.save()
        lugar2 = Lugar(
            configuracion_encuentro_id=cfg1.pk, lugar="piedragogico"
        )
        lugar2.save()
        ocupacion1 = Ocupacion(
            configuracion_encuentro_id=cfg1.pk, ocupacion="vagabundo"
        )
        ocupacion1.save()
        ocupacion2 = Ocupacion(
            configuracion_encuentro_id=cfg1.pk, ocupacion="academico"
        )
        ocupacion2.save()
        self.assertEqual(cfg1.to_dict(), expected_result)
