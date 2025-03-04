from django.shortcuts import render
from .models import *

# Create your views here.
def lista_eventos(request):
    eventos = Evento.objects.all()

    context = {
        'eventos': eventos,
    }
    return render(request, 'agenda.html',context)