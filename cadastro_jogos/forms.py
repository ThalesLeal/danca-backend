from django import forms
from .models import UsuarioJogos
from .utils import PERFIL_CHOICES

class UsuarioJogosForm(forms.ModelForm):
    class Meta:
        model = UsuarioJogos
        fields = ['nome', 'cpf', 'email', 'telefone', 'perfil']
        labels = {
            'nome': 'Nome Completo',
            'cpf': 'CPF',
            'email': 'Email',
            'telefone': 'Telefone',
            'perfil': 'perfil',
        }

        perfil = forms.ChoiceField(
            choices=PERFIL_CHOICES,
            widget=forms.Select(attrs={'class': 'form-control'})
        )
        
        widgets = {
            'nome_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control mask-cpf'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control mask-telefone'}),
            'perfil': forms.Select(attrs={'class': 'form-select'}),  
        }