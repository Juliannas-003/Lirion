from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from livros.models import Livro, StatusLeitura
from anotacoes.models import Anotacao
from services.ia import gerar_retrato, gerar_plano_leitura
from .models import Retrato, PlanoLeitura, PlanoGenero, PlanoLivroSugerido
from .forms import PlanoLeituraForm


@login_required
def ver_retrato(request, livro_id):
    """
    Exibe o retrato emocional de uma leitura concluída.
    Se ainda não existe, tenta gerar agora.
    """
    livro = get_object_or_404(Livro, id=livro_id)

    # Tenta buscar retrato existente primeiro
    retrato = Retrato.objects.filter(
        usuario=request.user, livro=livro
    ).first()

    if not retrato:
        # Não existe ainda — tenta gerar
        anotacoes = Anotacao.objects.filter(
            usuario=request.user, livro=livro
        )
        if not anotacoes.exists():
            messages.warning(
                request,
                'Não há anotações para gerar o retrato. '
                'Registre suas impressões durante a leitura.'
            )
            return redirect('anotacoes:pagina_livro', livro_id=livro_id)

        conteudo = gerar_retrato(anotacoes, livro.titulo, livro.autor)

        if conteudo:
            retrato = Retrato.objects.create(
                usuario=request.user,
                livro=livro,
                conteudo=conteudo
            )
            messages.success(request, 'Retrato emocional gerado!')
        else:
            messages.error(
                request,
                'Não foi possível gerar o retrato agora. '
                'Tente novamente em instantes.'
            )
            return redirect('anotacoes:pagina_livro', livro_id=livro_id)

    return render(request, 'retratos/ver_retrato.html', {
        'livro': livro,
        'retrato': retrato,
    })


@login_required
def criar_plano(request):
    """
    Formulário de criação do plano de leitura mensal.
    Coleta inputs, calcula tempo, chama IA e salva em três tabelas.
    """
    if request.method == 'POST':
        form = PlanoLeituraForm(request.POST)
        if form.is_valid():
            paginas_por_hora = form.cleaned_data['paginas_por_hora']
            horas_por_dia    = form.cleaned_data['horas_por_dia']
            quantidade_livros = form.cleaned_data['quantidade_livros']
            generos          = form.cleaned_data.get('generos', [])
            texto_livre      = form.cleaned_data.get('texto_livre', '')

            conteudo, duracao = gerar_plano_leitura(
                usuario=request.user,
                paginas_por_hora=paginas_por_hora,
                horas_por_dia=horas_por_dia,
                quantidade_livros=quantidade_livros,
                generos=generos,
                texto_livre=texto_livre
            )

            if conteudo:
                # Salva o plano principal
                plano = PlanoLeitura.objects.create(
                    usuario=request.user,
                    paginas_por_hora=paginas_por_hora,
                    horas_por_dia=horas_por_dia,
                    quantidade_livros=quantidade_livros,
                    texto_livre=texto_livre,
                    conteudo_ia=conteudo,
                    duracao_estimada_dias=duracao
                )

                # Salva os gêneros selecionados
                for genero in generos:
                    PlanoGenero.objects.create(
                        plano=plano,
                        genero=genero
                    )

                messages.success(request, 'Plano de leitura gerado!')
                return redirect('retratos:ver_plano', plano_id=plano.id)
            else:
                messages.error(
                    request,
                    'Não foi possível gerar o plano agora. Tente em instantes.'
                )
    else:
        form = PlanoLeituraForm()

    return render(request, 'retratos/criar_plano.html', {'form': form})


@login_required
def ver_plano(request, plano_id):
    plano = get_object_or_404(PlanoLeitura, id=plano_id, usuario=request.user)
    generos = plano.generos.all()
    return render(request, 'retratos/ver_plano.html', {
        'plano': plano,
        'generos': generos,
    })


@login_required
def historico_planos(request):
    planos = PlanoLeitura.objects.filter(
        usuario=request.user
    ).prefetch_related('generos')
    return render(request, 'retratos/historico.html', {'planos': planos})