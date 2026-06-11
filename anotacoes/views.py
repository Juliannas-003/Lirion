from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Anotacao
from .forms import AnotacaoForm
from livros.models import Livro, StatusLeitura


@login_required
def pagina_livro(request, livro_id):
    # Busca o livro e retorna o erro caso não encontre
    livro = get_object_or_404(Livro, id=livro_id)

    # Verificar se o livro pertence ao usuário (tem status de leitura)
    status_leitura = StatusLeitura.objects.filter(
        usuario=request.user,
        livro=livro
    ).first()

    # Buscar anotações do usuário logado pra o livro específico, ordenadas da mais recente para a mais antiga
    # O ordering do model já garante ordem decrescente
    anotacoes = Anotacao.objects.filter(
        usuario=request.user,
        livro=livro
    )

    form = AnotacaoForm()

    return render(request, 'anotacoes/pagina_livro.html', {
        'livro': livro,
        'anotacoes': anotacoes,
        'form': form,
        'status_leitura': status_leitura,
    })


@login_required
def salvar_anotacao(request, livro_id):
    if request.method != 'POST':
        return redirect('anotacoes:pagina_livro', livro_id=livro_id)

    livro = get_object_or_404(Livro, id=livro_id)
    form = AnotacaoForm(request.POST)

    if form.is_valid():
        anotacao = form.save(commit=False)
        anotacao.usuario = request.user
        anotacao.livro = livro
        anotacao.save()
        messages.success(request, 'Anotação salva!')
    else:
        messages.error(request, 'Não foi possível salvar. Verifique o texto.')

    return redirect('anotacoes:pagina_livro', livro_id=livro_id)


@login_required
def editar_anotacao(request, pk):
    # erro caso o usuário tente editar uma anotação que não é dele ou que não existe
    anotacao = get_object_or_404(Anotacao, pk=pk, usuario=request.user)

    if request.method == 'POST':
        form = AnotacaoForm(request.POST, instance=anotacao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Anotação atualizada!')
            return redirect('anotacoes:pagina_livro', livro_id=anotacao.livro.id)
    else:
        # Preenche o formulário com o texto atual da anotação
        form = AnotacaoForm(instance=anotacao)

    return render(request, 'anotacoes/editar.html', {
        'form': form,
        'anotacao': anotacao,
    })


@login_required
def deletar_anotacao(request, pk):
    anotacao = get_object_or_404(Anotacao, pk=pk, usuario=request.user)

    if request.method == 'POST':
        livro_id = anotacao.livro.id
        anotacao.delete()
        messages.success(request, 'Anotação removida.')
        return redirect('anotacoes:pagina_livro', livro_id=livro_id)

    # GET — mostra a tela de confirmação antes de deletar
    return render(request, 'anotacoes/confirmar_delete.html', {
        'anotacao': anotacao
    })


@login_required
def concluir_leitura(request, livro_id):
    if request.method != 'POST':
        return redirect('anotacoes:pagina_livro', livro_id=livro_id)

    livro = get_object_or_404(Livro, id=livro_id)

    # Verifica se tem anotações antes de concluir
    
    anotacoes = Anotacao.objects.filter(usuario=request.user, livro=livro)
    if not anotacoes.exists():
        messages.warning(
            request,
            'Adicione pelo menos uma anotação antes de concluir a leitura. '
            'As anotações são usadas para gerar seu retrato emocional.'
        )
        return redirect('anotacoes:pagina_livro', livro_id=livro_id)

    # mudando o status para lido2
    StatusLeitura.objects.filter(
        usuario=request.user,
        livro=livro
    ).update(status='lido')

    messages.success(
        request,
        f'"{livro.titulo}" marcado como lido! '
        'O retrato emocional estará disponível em breve.'
    )
    return redirect('livros:estante')
