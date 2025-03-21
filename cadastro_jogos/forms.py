from django import forms
from .models import UsuarioJogos, Regional, UsuarioRegional
from .utils import PERFIL_CHOICES
import re

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
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control mask-cpf'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control mask-telefone'}),
            'perfil': forms.Select(attrs={'class': 'form-select'}),  
        }

    def clean_nome(self):
        nome = self.cleaned_data['nome']
        if len(nome) < 3:
            raise forms.ValidationError("O nome deve ter pelo menos 3 caracteres.")
        return nome

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        cpf = re.sub(r'\D', '', cpf)  # Remove caracteres não numéricos do CPF
        if UsuarioJogos.objects.filter(cpf=cpf).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("CPF já cadastrado.")
        return cpf

class RegionalForm(forms.ModelForm):
    class Meta:
        model = Regional
        fields = ['nome', 'numero', 'cidade', 'tipo_regional']
        widgets = {
            'tipo_regional': forms.Select(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.NumberInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nome': 'Nome da Regional',
            'numero': 'Número',
            'cidade': 'Cidade',
            'tipo_regional': 'Tipo de Regional',
        }
    def clean_numero(self):
        numero = self.cleaned_data.get('numero')
        if numero is not None and (numero < 1 or numero > 99):
            raise forms.ValidationError("Erro: O número da regional deve estar entre 1 e 99, e deve ser inteiro.")
        return numero


class UsuarioRegionalForm(forms.ModelForm):
    class Meta:
        model = UsuarioRegional
        fields = ['usuario', 'data_inicio', 'data_fim', 'regional']
        widgets = {
            'regional': forms.HiddenInput(),
        }
        labels = {
            'usuario': 'Usuário',
            'data_inicio': 'Data de Início',
            'data_fim': 'Data de Fim',
            'regional': 'Regional',
        }
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-select'}),
            'data_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'regional': forms.Select(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "instance" in kwargs and kwargs["instance"]:
            self.fields["regional"].initial = kwargs["instance"].regional
        self.fields["regional"].widget = forms.HiddenInput()