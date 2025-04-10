from django.db.models import Sum
from .models import Evento, InscricaoEvento, ProfissionalEvento

def atualizar_contador_evento(evento_id):
    evento = Evento.objects.get(id=evento_id)
    evento.contador_inscricoes = (
        InscricaoEvento.objects.filter(evento=evento, confirmar=True).count() +
        ProfissionalEvento.objects.filter(evento=evento, confirmar=True).count()
    )
    evento.save()

def atualizar_valor_arrecadado(evento_id):
    evento = Evento.objects.get(id=evento_id)
    valor_total = sum(
        (evento.evento.valor_unitario or 0) 
        for evento in InscricaoEvento.objects.filter(evento=evento, confirmar=True)
    )
    evento.valor_arrecadado = valor_total
    evento.save()

def verificar_vagas_disponiveis(evento):
    if evento.quantidade_pessoas is not None:
        return max(0, evento.quantidade_pessoas - evento.contador_inscricoes)
    return None

def calcular_percentual_preenchimento(evento):
    if evento.quantidade_pessoas is not None and evento.quantidade_pessoas > 0:
        return (evento.contador_inscricoes / evento.quantidade_pessoas) * 100
    return 0