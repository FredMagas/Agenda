from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse
from .forms import UserRegistrationForm
from .models import *

# Create your views here.~

def index(request):
    usuario = request.user

    context = {
        'usuario': usuario,
    }

    return render(request, 'index.html', context)

def registro(request):
    return render(request, 'registro_usuario.html')

def submit_registro(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Render the registration pending page
            return render(request, 'registro_sucesso.html')  
        else:
            return render(request, 'registro_usuario.html', {'form': form})
    return render(request, 'registro_usuario.html')

# def registro_sucesso(request):
#     return render(request, 'registro_sucesso.html')

def login_user(request):
    return render( request, 'login.html')

def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/agenda/')
        else:
            messages.error(request, 'Usuário ou senha inválidos!')
    return redirect('/login/')

def logout_user(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/login/')
def lista_eventos(request):
    usuario = request.user
    data_atual = datetime.now() - timedelta(hours=1)
    eventos = Evento.objects.filter(usuario=usuario, 
                                    data_evento__gt=data_atual)

    context = {
        'eventos': eventos,
        'usuario': usuario,
    }
    return render(request, 'agenda.html',context)

@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {'usuario': request.user}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)

    return render(request, 'evento.html', dados)

@login_required(login_url='/login/')
def evento_historico(request):
    usuario = request.user
    data_atual = datetime.now() - timedelta(hours=1)
    eventos = Evento.objects.filter(usuario=usuario, 
                                    data_evento__lt=data_atual)

    context = {
        'eventos': eventos,
        'usuario': usuario,
    }
    return render(request, 'evento_historico.html',context)

@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        local = request.POST.get('local')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        usuario = request.user
        id_evento = request.POST.get('id_evento')
        if id_evento:
            evento = Evento.objects.get(id=id_evento)
            if evento.usuario == usuario:
                evento.titulo = titulo
                evento.local = local
                evento.data_evento = data_evento
                evento.descricao = descricao
                evento.save()
        else:
            Evento.objects.create(titulo=titulo,
                                local=local,
                                data_evento=data_evento,
                                descricao=descricao,
                                usuario=usuario,)
        return redirect('/agenda/')
    return redirect('/agenda/')

@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario = request.user
    try:
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        raise Http404()
    if usuario == evento.usuario:
        evento.delete()
    else:
        raise Http404()
    return redirect('/')

@login_required(login_url='/login/')
def json_lista_eventos(request):
    usuario = request.user
    evento = Evento.objects.filter(usuario=usuario).values('id', 'titulo')

    return JsonResponse(list(evento), safe=False)