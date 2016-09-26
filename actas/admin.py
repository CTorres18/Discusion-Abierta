# -*- coding: utf-8 -*-
from django.contrib import admin
from actas.read_only_admin import ReadOnlyModelAdmin

from .models import Tema, ItemTema, Ocupacion, Origen, ConfiguracionEncuentro, Lugar, TipoEncuentro, Encuentro, \
    Respuesta, Participante, ActaGuardada


class TemaAdmin(ReadOnlyModelAdmin):
    pass


class ItemTemaAdmin(ReadOnlyModelAdmin):
    pass


class OrigenAdmin(ReadOnlyModelAdmin):
    pass


class LugarAdmin(ReadOnlyModelAdmin):
    pass


class OcupacionAdmin(ReadOnlyModelAdmin):
    pass


class TipoEncuentroAdmin(ReadOnlyModelAdmin):
    pass


class EncuentroAdmin(ReadOnlyModelAdmin):
    pass


class ConfiguracionEncuentroAdmin(ReadOnlyModelAdmin):
    pass


class RespuestasAdmin(ReadOnlyModelAdmin):
    pass


class ParticipanteAdmin(ReadOnlyModelAdmin):
    pass

class ActaGuardadaAdmin(ReadOnlyModelAdmin):
    pass


admin.site.register(ActaGuardada,ActaGuardadaAdmin)
admin.site.register(ConfiguracionEncuentro, ItemTemaAdmin)
admin.site.register(Tema, TemaAdmin)
admin.site.register(Ocupacion, OcupacionAdmin)
admin.site.register(Origen, ItemTemaAdmin)
admin.site.register(Lugar, ItemTemaAdmin)
admin.site.register(TipoEncuentro, ItemTemaAdmin)
admin.site.register(Encuentro, EncuentroAdmin)
admin.site.register(ItemTema, ItemTemaAdmin)
admin.site.register(Respuesta, RespuestasAdmin)
admin.site.register(Participante, ParticipanteAdmin)
