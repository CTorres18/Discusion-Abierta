# -*- coding: utf-8 -*-
from actas.models import *

__author__ = 'Nicolas'


def init_db():
    cfg1 = ConfiguracionEncuentro(organizador="doge", descripcion="pene")
    cfg1.save()
    tema1 = Tema(
        configuracion_encuentro_id=cfg1.pk,
        tema="caquita",
        contexto="dcc",
        orden=2
    )
    tema1.save()
    item1_tema1 = ItemTema(
        tema_id=tema1.pk,
        pregunta="doge se la come?", pregunta_propuesta=u"Â¿atravesada? Â¿a dos manos?")
    item1_tema1.save()
    item2_tema1 = ItemTema(
        tema_id=tema1.pk,
        pregunta="hihose la come?",
        pregunta_propuesta=u"Â¿atravesada? Â¿a dos manos?"
    )
    item2_tema1.save()
    tema2 = Tema(
        configuracion_encuentro_id=cfg1.pk,
        tema="caquita2",
        contexto="dcc2",
        orden=1
    )
    tema2.save()
    item2_tema2 = ItemTema(
        tema_id=tema2.pk,
        pregunta="doge2 se la come?",
        pregunta_propuesta=u"Â¿atravesada2? Â¿a dos manos2?"
    )
    item2_tema2.save()
    item2_tema12 = ItemTema(
        tema_id=tema2.pk,
        pregunta="hihose la come2?",
        pregunta_propuesta=u"Â¿atravesada2? Â¿a dos manos2?"
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
    return cfg1
