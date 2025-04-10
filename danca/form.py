from django import forms
from django.core.exceptions import ValidationError
from .models import Lote,Categoria,TipoEvento,Evento,Camisa,Planejamento

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

class CamisaForm(forms.ModelForm):
    class Meta:
        model = Camisa
        fields = ['descricao', 'tipo', 'quantidade', 'valor_unitario']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descrição da Camisa'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': 'Quantidade em estoque'}),
            'valor_unitario': forms.TextInput(attrs={'class': 'form-control mask-valor', 'placeholder': 'R$ 0,00'}),
        }
        labels = {
            'descricao': 'Descrição da Camisa',
            'tipo': 'Tipo',
            'quantidade': 'Quantidade em Estoque',
            'valor_unitario': 'Valor Unitário',
        }
    def clean_quantidade(self):
        """
        Valida o campo quantidade para garantir que seja maior ou igual a zero.
        """
        quantidade = self.cleaned_data.get('quantidade')
        if quantidade is not None and quantidade < 0:
            raise ValidationError("A quantidade não pode ser negativa.")
        return quantidade

    def clean_valor_unitario(self):
        """
        Valida o campo valor_unitario para garantir que seja maior ou igual a zero.
        """
        valor_unitario = self.cleaned_data.get('valor_unitario')
        if valor_unitario is not None and valor_unitario < 0:
            raise ValidationError("O valor unitário não pode ser negativo.")
        return valor_unitario


class PlanejamentoForm(forms.ModelForm):
    class Meta:
        model = Planejamento
        fields = ['descricao', 'valor_planejado']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descrição do Planejamento'}),
            'valor_planejado': forms.TextInput(attrs={'class': 'form-control mask-valor', 'placeholder': 'R$ 0,00'}),
        }
        labels = {
            'descricao': 'Descrição do Planejamento',
            'valor_planejado': 'Valor Planejado',
        }

    def clean_valor_planejado(self):
        """
        Valida o campo valor_planejado para garantir que seja maior ou igual a zero.
        """
        valor_planejado = self.cleaned_data.get('valor_planejado')
        if valor_planejado is not None and valor_planejado < 0:
            raise ValidationError("O valor planejado não pode ser negativo.")
        return valor_planejado