from django.contrib import admin
from .models import *

# Register your models here.

class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_evento', 'data_criacao')

admin.site.register(Evento, EventoAdmin)