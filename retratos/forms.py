from django import forms

GENEROS_CHOICES = [
    ('ficcao_cientifica', 'Ficção Científica'),
    ('fantasia', 'Fantasia'),
    ('romance', 'Romance'),
    ('terror', 'Terror'),
    ('thriller', 'Thriller / Suspense'),
    ('literario', 'Literatura Contemporânea'),
    ('policial', 'Policial'),
    ('historico', 'Romance Histórico'),
    ('nao_ficcao', 'Não-Ficção'),
    ('biografia', 'Biografia / Memórias'),
    ('autoajuda', 'Autoajuda / Desenvolvimento'),
    ('poesia', 'Poesia'),
    ('distopia', 'Distopia'),
    ('contos', 'Contos'),
]

class PlanoLeituraForm(forms.Form):
    paginas_por_hora = forms.FloatField(
        label='Quantas páginas você lê por hora?',
        min_value=5,
        max_value=200,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: 30'
        })
    )
    horas_por_dia = forms.FloatField(
        label='Quantas horas por dia você tem para ler?',
        min_value=0.25,
        max_value=12,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: 1.5'
        })
    )
    quantidade_livros = forms.IntegerField(
        label='Quantos livros quer ler no mês?',
        min_value=1,
        max_value=8,
        initial=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control'
        })
    )
    generos = forms.MultipleChoiceField(
        choices=GENEROS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Gêneros de interesse'
    )
    texto_livre = forms.CharField(
        required=False,
        label='Conte mais sobre o que você quer ler',
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'form-control'
            # pensar em um placeholder para esse campo 
        })
    )