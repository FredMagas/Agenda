from django.contrib import admin
from .models import *

# Register your models here.

class EventoAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'data_evento', 'data_criacao')
    list_filter = ['usuario', 'data_evento',]

admin.site.register(Evento, EventoAdmin)