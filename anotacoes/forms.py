from django import forms
from .models import Anotacao


class AnotacaoForm(forms.ModelForm):
    class Meta:
        model = Anotacao
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={
                'placeholder': 'O que você está pensou, sentiu ou se questionou ao ler este livro agora?',
                'rows': 4,
                'class': 'form-control',
            })
        }
        labels = {
            'texto': ''
        }