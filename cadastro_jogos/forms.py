from django import forms
from .models import Instituicao, UsuarioJogos, Regional, UsuarioRegional
from .utils import PERFIL_CHOICES
import re
from django.core.exceptions import ValidationError

class UsuarioJogosForm(forms.ModelForm):
    class Meta:
        model = UsuarioJogos
        fields = ['nome', 'cpf', 'email', 'telefone', 'perfil']
        labels = {
            'nome': 'Nome Completo',
            'cpf': 'CPF',
            'email': 'E-mail',
            'telefone': 'Telefone',
            'perfil': 'Perfil',
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
            raise ValidationError("O nome deve ter pelo menos 3 caracteres.")
        return nome

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        cpf = re.sub(r'\D', '', cpf)  # Remove caracteres não numéricos do CPF
        if UsuarioJogos.objects.filter(cpf=cpf).exclude(id=self.instance.id).exists():
            raise ValidationError("CPF já cadastrado.")
        return cpf  
    

class RegionalForm(forms.ModelForm):
    class Meta:
        model = Regional
        fields = ['nome', 'numero', 'cidade', 'tipo_regional']
        widgets = {
            'tipo_regional': forms.Select(attrs={'class': 'form-select'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 99}),
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
            raise ValidationError("O número da regional deve estar entre 1 e 99, e deve ser inteiro.")
        return numero


class UsuarioRegionalForm(forms.ModelForm):
    class Meta:
        model = UsuarioRegional
        fields = ['usuario', 'data_inicio', 'data_fim', 'regional']
        labels = {
            'usuario': 'Usuário',
            'data_inicio': 'Data de Início',
            'data_fim': 'Data de Fim',
            'regional': 'Regional',
        }
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-select'}),
            'data_inicio': forms.DateInput(format=('%Y-%m-%d'), attrs={'class': 'form-control', 'type': 'date'}),
            'data_fim': forms.DateInput(format=('%Y-%m-%d'), attrs={'class': 'form-control', 'type': 'date'}),
            'regional': forms.Select(attrs={'class': 'form-select disabled'}),
        }
    def __init__(self, *args, **kwargs):
        regional = kwargs.pop('regional', None)
        instance = kwargs.get("instance", None)

        super().__init__(*args, **kwargs)

        self.fields["regional"].initial = regional

        if instance:
            self.fields['usuario'].initial = instance.usuario
        else:
            self.fields["usuario"].queryset = UsuarioJogos.objects.exclude(
                id__in=UsuarioRegional.objects.values_list("usuario", flat=True)
            )

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get("data_inicio")
        data_fim = cleaned_data.get("data_fim")
        usuario = cleaned_data.get("usuario")
        regional = cleaned_data.get("regional")
    
        if self.instance.pk:
            if usuario != self.instance.usuario:
                raise ValidationError("Você não pode alterar o usuário associado a este registro.")
            if regional != self.instance.regional:
                raise ValidationError("Você não pode alterar a regional associada a este registro.")

        if data_inicio and data_fim and data_fim <= data_inicio:
            raise ValidationError("A data de fim deve ser maior que a data de início.")
   
        return cleaned_data


class InstituicaoForm(forms.ModelForm):
    class Meta:
        model = Instituicao
        fields = [
            'nome', 'cep', 'logradouro', 
            'numero', 'bairro', 'municipio',
            'complemento', 'pertence_a_regional',
            'cpf_cnpj', 'tipo_regional', 'regional', 'rede_ensino'
        ]
        labels = {
            'nome': 'Nome da Instituição',
            'cep': 'CEP',
            'logradouro': 'Logradouro',
            'numero': 'Número',
            'bairro': 'Bairro',
            'municipio': 'Município',
            'complemento': 'Complemento',
            'pertence_a_regional': 'Pertence à Regional?',
            'cpf_cnpj': 'CPF/CNPJ',
            'tipo_regional': 'Tipo de Regional',
            'regional': 'Regional',
            'rede_ensino': 'Rede de Ensino'
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control mask-cep'}),
            'logradouro': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'municipio': forms.TextInput(attrs={'class': 'form-control'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control'}),
            'pertence_a_regional': forms.Select(attrs={'class': 'form-select'}, choices=[(True, "Sim"), (False, "Não")]),
            'cpf_cnpj': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_regional': forms.Select(attrs={'class': 'form-select'}),
            'regional': forms.Select(attrs={'class': 'form-select'}),
            'rede_ensino': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        pertence_a_regional = cleaned_data.get('pertence_a_regional')
        cpf_cnpj = cleaned_data.get('cpf_cnpj')
        tipo_regional = cleaned_data.get('tipo_regional')
        regional = cleaned_data.get('regional')
        rede_ensino = cleaned_data.get('rede_ensino')

        if cpf_cnpj:
            cpf_cnpj = re.sub(r'\D', '', cpf_cnpj)

        if pertence_a_regional:
            if not tipo_regional:
                raise ValidationError(
                    "Se a instituição pertence à uma regional, o tipo de regional é obrigatório."
                )
            if not regional:
                raise ValidationError(
                    "Se a instituição pertence à uma regional, a regional é obrigatória."
                )
            if not rede_ensino:
                raise ValidationError(
                    "Se a instituição pertence à uma regional, a rede de ensino é obrigatória."
                )
        return cleaned_data
    

    def clean_cpf_cnpj(self):
        cpf_cnpj = self.cleaned_data['cpf_cnpj']
        pertence_a_regional = self.cleaned_data['pertence_a_regional']

        if cpf_cnpj:
            cpf_cnpj = re.sub(r'\D', '', cpf_cnpj)
        if not pertence_a_regional and not cpf_cnpj:
            raise ValidationError(
                "O CPF/CNPJ é obrigatório se a instituição não pertence à uma regional."
            )
        return cpf_cnpj


