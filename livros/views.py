from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from services.openlibrary import buscar_livro
from .models import Livro, StatusLeitura


# =========================================================
# BUSCA DE LIVROSS
# ========================================================

@login_required
def buscar(request):
    livros = []
    termo = request.GET.get('q', '').strip()

    if termo:
        livros = buscar_livro(termo)
        if not livros:
            messages.warning(
                request,
                f'Nenhum resultado para "{termo}". Tente outro termo.'
            )

    return render(request, 'livros/buscar.html', {
        'livros': livros,
        'termo': termo,
    })


# =============================================================
# ADD A ESTANTE E + ,
# =============================================================
@login_required
def adicionar(request):
    if request.method != 'POST':
        return redirect('livros:buscar')

    # DADOS do form do card de busca (hidden inputs)
    titulo   = request.POST.get('titulo', '').strip()
    autor    = request.POST.get('autor', '').strip()
    capa_url = request.POST.get('capa_url', '').strip()
    isbn     = request.POST.get('isbn', '').strip()
    ol_key   = request.POST.get('ol_key', '').strip()
    ano      = request.POST.get('ano') or None
    status   = request.POST.get('status', 'quero_ler')

    if not titulo:
        messages.error(request, 'Título do livro não encontrado.')
        return redirect('livros:buscar')

    # criação ou get livros
    livro, _ = Livro.objects.get_or_create(
        titulo=titulo,
        autor=autor,
        defaults={
            'capa_url': capa_url,
            'isbn':     isbn,
            'ol_key':   ol_key,
            'ano':      ano,
        }
    )

    # criar ou atualizar status da leitura
    status_obj, criado = StatusLeitura.objects.get_or_create(
        usuario=request.user,
        livro=livro,
        defaults={'status': status}
    )

    if not criado:
        status_obj.status = status
        status_obj.save()
        messages.info(
            request,
            f'"{titulo}" já estava na sua estante. Status atualizado para '
            f'{status_obj.get_status_display()}.'
        )
    else:
        messages.success(
            request,
            f'"{titulo}" adicionado à sua estante como '
            f'{status_obj.get_status_display()}!'
        )

    return redirect('livros:estante')


# ======================================================
# ESTANTE DO USUÁRIO
# ======================================================
@login_required
def estante(request):
    #  FILTrar por usuário sempre
    lendo     = StatusLeitura.objects.filter(
        usuario=request.user, status='lendo'
    ).select_related('livro')

    lidos     = StatusLeitura.objects.filter(
        usuario=request.user, status='lido'
    ).select_related('livro')

    quero_ler = StatusLeitura.objects.filter(
        usuario=request.user, status='quero_ler'
    ).select_related('livro')

    return render(request, 'livros/estante.html', {
        'lendo':     lendo,
        'lidos':     lidos,
        'quero_ler': quero_ler,
    })


# ========================================================
# REMOÇÃO DE ESTANTE
# ========================================================


@login_required
def remover(request, status_id):
    # Filtra por usuario=request.user para garantir que
    # o usuário remove APENAS os seus próprios livros
    status_obj = get_object_or_404(
        StatusLeitura,
        id=status_id,
        usuario=request.user
    )
    titulo = status_obj.livro.titulo
    status_obj.delete()
    messages.success(request, f'"{titulo}" removido da sua estante.')
    return redirect('livros:estante')


# ========================================================
# MUDAR STATUS
# ========================================================
@login_required
def mudar_status(request, status_id):
    if request.method != 'POST':
        return redirect('livros:estante')

    status_obj = get_object_or_404(
        StatusLeitura,
        id=status_id,
        usuario=request.user
    )
    novo_status = request.POST.get('status')
    if novo_status in ['lido', 'lendo', 'quero_ler']:
        status_obj.status = novo_status
        status_obj.save()
        messages.success(
            request,
            f'Status de "{status_obj.livro.titulo}" atualizado!'
        )
    return redirect('livros:estante')