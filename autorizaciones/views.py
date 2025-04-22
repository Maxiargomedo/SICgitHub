from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm
from .models import Solicitud

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def historial_solicitudes(request):
    solicitudes = Solicitud.objects.filter(usuario=request.user)
    return render(request, 'historial.html', {'solicitudes': solicitudes})