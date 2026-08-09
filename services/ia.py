from google import genai
from django.conf import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)

# substituição do getmodel antigo (variável model name e função generate
MODEL_NAME = "gemini-3.5-flash"

def _generate(prompt):
    return client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )


def gerar_retrato(anotacoes, titulo_livro, autor_livro=''):
    
    #Gera retrato a partir das anotações das leituras 
    
    if not anotacoes:
        return None

    # Pega as anotações em ordem cronológica inversa (mais recentes primeiro)
    # O ordering do model já garante isso
    textos = '\n'.join([f'- {a.texto}' for a in anotacoes])

    autor_info = f' de {autor_livro}' if autor_livro else ''

    prompt = f"""
Você é um assistente literário sensível, capaz de capturar emoções dos leitoes, baseados em suas notas de leitura .

Um leitor acabou de terminar "{titulo_livro}"{autor_info}.
Durante a leitura, registrou estas anotações pessoais:

{textos}

Com base nessas anotações, crie um retrato emocional personalizado.

## O retrato deve:
- Identificar os temas que apareceram com mais frequência
- Perceber padrões observados nas notas do leitor específico
- Reconhecer o tom emocional predominante nas anotações do leitor
- Apontar perguntas ou inquietações que o leitor levantou
- Terminar com uma frase síntese que capture a essência da experiência

## Instruções mais diretas para a criação do retrato 
Escreva em segunda pessoa (você), de forma calorosa e reflexiva.
Máximo 200 palavras, para ser um resumo eficiente. 
Não faça uma análise fria, escreva como alguém que conhece os padrões dos leitores.

    """


    try:
        resposta = _generate(prompt)
        return resposta.text

    except Exception as e:
        print(f'Erro Gemini API (retrato): {e}')
        return None


def gerar_plano_leitura(usuario, paginas_por_hora, horas_por_dia,
                        quantidade_livros, generos, texto_livre):
    """
    Gera plano de leitura mensal personalizado.
    Retorna string com o plano ou None em caso de erro.

    O cálculo de tempo é feito aqui antes de chamar a IA,
    para que o prompt seja mais preciso e realista.
    """
    from anotacoes.models import Anotacao
    from retratos.models import Retrato

    # Cálculo matemático do tempo disponível
    paginas_por_dia = paginas_por_hora * horas_por_dia
    # Estimativa de 250 páginas por livro (média de romance/ficção)
    paginas_totais_estimadas = 250 * quantidade_livros
    duracao_estimada = round(paginas_totais_estimadas / paginas_por_dia)

    # Histórico emocional dos últimos retratos
    retratos_recentes = Retrato.objects.filter(
        usuario=usuario
    ).order_by('-data_geracao')[:3]

    historico_emocional = ''
    if retratos_recentes:
        trechos = [
            f'- Após "{r.livro.titulo}": {r.conteudo[:150]}...'
            for r in retratos_recentes
        ]
        historico_emocional = '\n'.join(trechos)
    else:
        historico_emocional = 'Sem histórico de leituras anteriores ainda.'

    # Gêneros selecionados
    generos_texto = ', '.join(generos) if generos else 'sem preferência definida'

    prompt = f"""
Você é um curador literário especializado em planos de leitura personalizados.

PERFIL DO LEITOR:
- Velocidade de leitura: {paginas_por_hora} páginas/hora
- Tempo disponível: {horas_por_dia} horas/dia
- Isso equivale a: {paginas_por_dia:.0f} páginas/dia
- Meta: {quantidade_livros} livros no próximo mês
- Tempo total estimado disponível: {duracao_estimada} dias de leitura

PREFERÊNCIAS DE GÊNERO: {generos_texto}

CONTEXTO ADICIONAL DO LEITOR: {texto_livre if texto_livre else 'Nenhum contexto adicional.'}

HISTÓRICO EMOCIONAL RECENTE:
{historico_emocional}
   
TAREFA:
Crie um plano de leitura para o próximo mês com exatamente {quantidade_livros} livro(s).

Para cada livro forneça:
1. Título e autor completo
2. Número aproximado de páginas
3. Semana do mês para ler (1, 2, 3 ou 4)
4. Justificativa personalizada de 2 a 3 linhas conectando com o perfil desse leitor

REGRAS:
- Seja realista com o tempo disponível calculado acima
- Priorize autores brasileiros e obras menos conhecidas
- Evite bestsellers óbvios
- Considere o histórico emocional para sugerir progressão temática
- Escreva em português

Formate a resposta de forma clara com os livros numerados.
    """

    

    try:
        resposta = _generate(prompt)
        return resposta.text, duracao_estimada

    except Exception as e:
        print(f'Erro Gemini API (plano): {e}')
        return None, None