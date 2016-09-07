import json

from django.test.testcases import TransactionTestCase
from django.test import Client


class DatabaseToDictTests(TransactionTestCase):

    fixtures = [
        'test_configuracionencuentros.json',
        'test_temas.json',
        'test_itemtemas.json',
        'test_tipoencuentros.json',
        'test_origenes.json',
        'test_lugares.json',
        'test_ocupaciones.json',
    ]

    def test_database_to_dict(self):
        expected = {
            u'pk': 1,
            u'organizador': u'fake_organizador',
            u'max_participantes': 50,
            u'min_participantes': 3,
            u'participante_organizador': {},
            u'participantes': [{}, {}],
            u'origenes': [
                {u'pk': 1, u'nombre': u'Casa Central 1'},
                {u'pk': 2, u'nombre': u'FCFM 1'}
            ],
            u'lugares': [
                {u'pk': 1, u'nombre': u'Casa Central'},
                {u'pk': 2, u'nombre': u'FCFM'}
            ],
            u'temas': [
                {
                    u'pk': 1,
                    u'titulo': u'tema_1',
                    u'contextualizacion': u'DCC',
                    u'items': [
                        {u'pk': 1, u'pregunta_propuesta': u'Propuesta tema 1', u'pregunta': u'Preguta tema 1'}
                    ],
                },
                {
                    u'pk': 2,
                    u'titulo': u'tema_2',
                    u'contextualizacion': u'DCC 2',
                    u'items': [
                        {u'pk': 2, u'pregunta_propuesta': u'Propuesta tema 2', u'pregunta': u'Preguta tema 2'}
                    ],
                }
            ],
            u'tipos': [
                {u'pk': 1, u'nombre': u'A'},
                {u'pk': 2, u'nombre': u'B'}
            ],
            u'ocupaciones': [
                {u'pk': 1, u'nombre': u'Acad\xe9mico'},
                {u'pk': 2, u'nombre': u'Funcionario'}
            ]
        }
        self.maxDiff = None

        client = Client()
        response = client.get('/actas/base/1')

        self.assertEqual(expected, json.loads(response.content.decode('utf-8')))
