# -*- coding: utf-8 -*-

import json

from actas.models import *
from django.test import TestCase
from actas.test_helpers import init_db

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
        cfg1 = init_db()
        self.assertEqual(cfg1.to_dict(), expected_result)
