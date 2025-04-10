from django import forms
from django.core.exceptions import ValidationError
from .models import Lote,Categoria,TipoEvento,Evento

class LoteForm(forms.ModelForm):
    class Meta:
        model = Lote
        fields = ['descricao', 'valor_unitario', 'unidades', 'status']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descrição do lote'}),
            'valor_unitario': forms.TextInput(attrs={'class': 'form-control mask-valor', 'placeholder': 'R$ 0,00'}),
            'unidades': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': 'Quantidade'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'descricao': 'Descrição do Lote',
            'valor_unitario': 'Valor Unitário',
            'unidades': 'Quantidade de Unidades',
            'status': 'Status',
        }

    def clean_unidades(self):
        """
        Valida o campo unidades para garantir que seja maior que zero.
        """
        unidades = self.cleaned_data.get('unidades')
        if unidades is not None and unidades <= 0:
            raise ValidationError("A quantidade de unidades deve ser maior que zero.")
        return unidades


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['descricao']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descrição da categoria'}),
        }
        labels = {
            'descricao': 'Descrição da Categoria',
        }


class TipoEventoForm(forms.ModelForm):
    class Meta:
        model = TipoEvento
        fields = ['descricao']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descrição do Tipo de Evento'}),
        }
        labels = {
            'descricao': 'Descrição do Tipo de Evento',
        }

    
class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['descricao', 'tipo', 'data', 'quantidade_pessoas', 'valor_unitario', 'status']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descrição do Evento'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'data': forms.DateInput(attrs={'class': 'form-control mask-data', 'type': 'date'}),
            'quantidade_pessoas': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': 'Número de vagas'}),
            'valor_unitario': forms.TextInput(attrs={'class': 'form-control mask-valor', 'placeholder': 'R$ 0,00'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'descricao': 'Descrição do Evento',
            'tipo': 'Tipo de Evento',
            'data': 'Data do Evento',
            'quantidade_pessoas': 'Quantidade de Vagas',
            'valor_unitario': 'Valor Unitário',
            'status': 'Status do Evento',
        }

    def clean_quantidade_pessoas(self):
        """
        Valida o campo quantidade_pessoas para garantir que seja maior que zero.
        """
        quantidade_pessoas = self.cleaned_data.get('quantidade_pessoas')
        if quantidade_pessoas is not None and quantidade_pessoas <= 0:
            raise ValidationError("A quantidade de vagas deve ser maior que zero.")
        return quantidade_pessoas

    def clean_valor_unitario(self):
        """
        Valida o campo valor_unitario para garantir que seja maior ou igual a zero.
        """
        valor_unitario = self.cleaned_data.get('valor_unitario')
        if valor_unitario is not None and valor_unitario < 0:
            raise ValidationError("O valor unitário não pode ser negativo.")
        return valor_unitario