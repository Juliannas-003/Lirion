from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class UsuarioCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='E-mail') #email para permitir a recuperaçãopor email 

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class PerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['foto', 'bio', 'email']
        widgets = {
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={
                'rows': 4, 'class': 'form-control',
                'placeholder': 'Conte um pouco sobre você como leitor...'
            }),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        labels = {'foto': 'Foto de perfil', 'bio': 'Sobre você', 'email': 'E-mail'}