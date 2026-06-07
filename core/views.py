from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UsuarioCreationForm

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