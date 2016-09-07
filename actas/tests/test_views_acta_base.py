# -*- coding: utf-8 -*-
from django.test import Client
from django.test.testcases import TransactionTestCase
from django.test.utils import override_settings


class ViewsBaseTestCase(TransactionTestCase):

    fixtures = [
        'test_configuracionencuentros.json',
        'test_temas.json',
        'test_itemtemas.json',
        'test_tipoencuentros.json',
        'test_origenes.json',
        'test_lugares.json',
        'test_ocupaciones.json',
    ]

    def setUp(self):
        self.maxDiff = None
        self.client = Client()
        self.expected = {
            u'pk': 1,
            u'organizador': u'fake_organizador',
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
            ],
            u'participante_organizador': {}
        }

    def test_obtener_acta_base_defecto(self):

        expected_params = {
            u'min_participantes': 3,
            u'max_participantes': 50,
        }
        expected_params.update(self.expected)
        expected_params[u'participantes'] = [{} for i in range(expected_params['min_participantes'] - 1)]

        response = self.client.get('/actas/base/1')

        self.assertEquals(200, response.status_code)
        self.assertEquals(expected_params, response.json())

    def test_obtener_acta_base_settings_py(self):

        expected_params = {
            u'min_participantes': 5,
            u'max_participantes': 9,
        }
        expected_params.update(self.expected)
        expected_params['participantes'] = [{} for i in range(expected_params['min_participantes'] - 1)]

        with override_settings(DISCUSION_ABIERTA={'PARTICIPANTES_MIN': expected_params['min_participantes'], 'PARTICIPANTES_MAX': expected_params['max_participantes']}):
            response = self.client.get('/actas/base/1')
            self.assertEquals(200, response.status_code)
            self.assertEquals(expected_params, response.json())
