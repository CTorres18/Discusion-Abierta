# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Tema, ItemTema, Ocupacion, Origen, ConfiguracionEncuentro, Lugar, TipoEncuentro, Encuentro, \
    Respuesta


class TemaAdmin(admin.ModelAdmin):
    pass


class ItemTemaAdmin(admin.ModelAdmin):
    pass


class OrigenAdmin(admin.ModelAdmin):
    pass


class LugarAdmin(admin.ModelAdmin):
    pass


class OcupacionAdmin(admin.ModelAdmin):
    pass


class TipoEncuentroAdmin(admin.ModelAdmin):
    pass


class EncuentroAdmin(admin.ModelAdmin):
    pass


class ConfiguracionEncuentroAdmin(admin.ModelAdmin):
    pass


class RespuestasAdmin(admin.ModelAdmin):
    pass


admin.site.register(ConfiguracionEncuentro, ItemTemaAdmin)
admin.site.register(Tema, TemaAdmin)
admin.site.register(Ocupacion, OcupacionAdmin)
admin.site.register(Origen, ItemTemaAdmin)
admin.site.register(Lugar, ItemTemaAdmin)
admin.site.register(TipoEncuentro, ItemTemaAdmin)
admin.site.register(Encuentro, EncuentroAdmin)
admin.site.register(ItemTema, ItemTemaAdmin)
admin.site.register(Respuesta, RespuestasAdmin)
