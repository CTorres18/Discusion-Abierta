# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Tema, ItemTema


class TemaAdmin(admin.ModelAdmin):
    pass


class ItemAdmin(admin.ModelAdmin):
    pass


admin.site.register(Tema,TemaAdmin)
admin.site.register(ItemTema, ItemAdmin)
