from django import forms
from django.core.exceptions import ValidationError
from .models import Lote

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

    def clean_valor_unitario(self):
        """
        Valida o campo valor_unitario para garantir que seja maior que zero.
        """
        valor = self.cleaned_data.get('valor_unitario')
        if valor is not None:
            try:
                # Remove o prefixo "R$" e converte para float
                valor = float(str(valor).replace("R$", "").replace(".", "").replace(",", ".").strip())
            except ValueError:
                raise ValidationError("O valor unitário deve ser um número válido.")
            if valor <= 0:
                raise ValidationError("O valor unitário deve ser maior que zero.")
        return valor

    def clean_unidades(self):
        """
        Valida o campo unidades para garantir que seja maior que zero.
        """
        unidades = self.cleaned_data.get('unidades')
        if unidades is not None and unidades <= 0:
            raise ValidationError("A quantidade de unidades deve ser maior que zero.")
        return unidades