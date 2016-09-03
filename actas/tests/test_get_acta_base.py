import json
from actas.models import *
from django.test import TestCase
from django.test import Client
from actas.test_helpers import init_db


class DatabaseToDictTests(TestCase):
    def test_database_to_dict(self):
        expected_result = expected_result = {u"origenes": [{u"pk": 1, u"origen": u"fcfm"}, {u"pk": 2, u"origen": u"piedragogico"}], u"organizador": u"doge", u"participantes": [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}], u"min_participantes": 10, u"lugares": [{u"lugar": u"fcfm", u"pk": 1}, {u"lugar": u"piedragogico", u"pk": 2}], u"temas": [{u"pk": 2, u"items": [{u"pk": 3, u"pregunta_propuesta": u"\u00c2\u00bfatravesada2? \u00c2\u00bfa dos manos2?", u"pregunta": u"doge2 se la come?"}], u"tema": u"caquita2"}, {u"pk": 1, u"items": [{u"pk": 1, u"pregunta_propuesta": u"\u00c2\u00bfatravesada? \u00c2\u00bfa dos manos?", u"pregunta": u"doge se la come?"}, {u"pk": 2, u"pregunta_propuesta": u"\u00c2\u00bfatravesada? \u00c2\u00bfa dos manos?", u"pregunta": u"hihose la come?"}], u"tema": u"caquita"}], u"tipos": [{u"pk": 1, u"tipo": u"sensual"}, {u"pk": 2, u"tipo": u"sepsi"}], u"max_participantes": 50, u"pk": 1, u"ocupaciones": [{u"pk": 1, u"ocupacion": u"vagabundo"}, {u"pk": 2, u"ocupacion": u"academico"}]}
        init_db()
        c = Client()
        response = c.get('/actas/base/1')
        self.assertEqual(json.loads(response.content.decode('utf-8')), expected_result)