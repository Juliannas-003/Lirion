from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UsuarioCreationForm, PerfilForm 
from django.contrib.auth.decorators import login_required

def cadastro(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta criada com sucesso! Faça login.')
            return redirect('/accounts/login/')
    else:
        form = UsuarioCreationForm()
    return render(request, 'core/cadastro.html', {'form': form})

def home(request):
    return render(request, 'core/home.html')


@login_required
def perfil(request):
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado!')
            return redirect('perfil')
    else:
        form = PerfilForm(instance=request.user)
    return render(request, 'core/perfil.html', {'form': form})