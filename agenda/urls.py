"""
URL configuration for agenda project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core.views import *
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("agenda/", lista_eventos, name="agenda"),
    path("agenda/historico/", evento_historico, name="agenda_historico"),
    path("agenda/lista", json_lista_eventos, name="json_agenda"),
    path("agenda/evento/", evento, name="evento"),
    path("agenda/evento/submit", submit_evento, name="evento"),
    path("agenda/evento/delete/<int:id_evento>", delete_evento, name="delete_evento"),
    path("", RedirectView.as_view(url='/agenda/')),
    path("login/", login_user, name="login"),
    path("login/submit", submit_login, name="submit_login"),
    path("logout/", logout_user, name="logout_user"),
]
