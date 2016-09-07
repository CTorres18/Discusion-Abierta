# -*- coding: utf-8 -*-
from django.test.testcases import TransactionTestCase

from actas.models import ConfiguracionEncuentro


__author__ = 'Nicolás Varas'


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

        self.maxDiff = None

        expected = {
            'pk': 1,
            'organizador': u'fake_organizador',
            'origenes': [
                {'pk': 1, 'nombre': u'Casa Central 1'},
                {'pk': 2, 'nombre': u'FCFM 1'}
            ],
            'lugares': [
                {'pk': 1, 'nombre': u'Casa Central'},
                {'pk': 2, 'nombre': u'FCFM'}
            ],
            'temas': [
                {
                    'pk': 1,
                    'titulo': u'tema_1',
                    'contextualizacion': u'DCC',
                    'items': [
                        {'pk': 1, 'pregunta_propuesta': u'Propuesta tema 1', 'pregunta': u'Preguta tema 1'}
                    ],
                },
                {
                    'pk': 2,
                    'titulo': u'tema_2',
                    'contextualizacion': u'DCC 2',
                    'items': [
                        {'pk': 2, 'pregunta_propuesta': u'Propuesta tema 2', 'pregunta': u'Preguta tema 2'}
                    ],
                }
            ],
            'tipos': [
                {'pk': 1, 'nombre': u'A'},
                {'pk': 2, 'nombre': u'B'}
            ],
            'ocupaciones': [
                {'pk': 1, 'nombre': u'Acad\xe9mico'},
                {'pk': 2, 'nombre': u'Funcionario'}
            ]
        }

        actual = ConfiguracionEncuentro.objects.get(pk=1)

        self.assertEqual(expected, actual.to_dict())
