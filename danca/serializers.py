from rest_framework import serializers
from .models import Categoria, Evento, Camisa, Planejamento, Inscricao, Profissional, Entrada, Saida, Pagamento, TipoEvento, Lote


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ["id", "descricao"]


class TipoEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEvento
        fields = ["id", "descricao"]


class EventoSerializer(serializers.ModelSerializer):
    tipo_descricao = serializers.CharField(source="tipo.descricao", read_only=True)

    class Meta:
        model = Evento
        fields = [
            "id",
            "descricao",
            "tipo",
            "tipo_descricao",
            "data",
            "quantidade_pessoas",
            "valor_unitario",
            "contador_inscricoes",
            "status",
        ]


class CamisaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camisa
        fields = [
            "id",
            "tipo",
            "descricao",
            "quantidade",
            "valor_compra",
            "valor_venda",
            "data_cadastro",
        ]


class PlanejamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planejamento
        fields = [
            "id",
            "descricao",
            "valor_planejado",
            "valor_pago",
            "valor_restante",
            "status",
        ]
        read_only_fields = ["valor_pago", "valor_restante", "status"]


class InscricaoSerializer(serializers.ModelSerializer):
    categoria_descricao = serializers.CharField(source="categoria.descricao", read_only=True)
    foto_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Inscricao
        fields = [
            "id",
            "nome",
            "cpf",
            "categoria",
            "categoria_descricao",
            "cep",
            "municipio",
            "uf",
            "lote",
            "desconto",
            "numero_parcelas",
            "valor_total",
            "foto",
            "foto_url",
        ]
    
    def get_foto_url(self, obj):
        if obj.foto and hasattr(obj.foto, 'url'):
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.foto.url)
        return None


class ProfissionalSerializer(serializers.ModelSerializer):
    funcao_descricao = serializers.CharField(source="funcao.descricao", read_only=True)
    foto_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Profissional
        fields = [
            "id",
            "nome",
            "cpf",
            "funcao",
            "funcao_descricao",
            "valor_hora_aula",
            "qt_aulas",
            "local_partida",
            "local_volta",
            "foto",
            "foto_url",
        ]
    
    def get_foto_url(self, obj):
        if obj.foto and hasattr(obj.foto, 'url'):
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.foto.url)
        return None


class EntradaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrada
        fields = [
            "id",
            "descricao",
            "valor",
            "data",
        ]


class SaidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saida
        fields = [
            "id",
            "descricao",
            "valor",
            "data",
        ]


class PagamentoSerializer(serializers.ModelSerializer):
    tipo_modelo = serializers.ChoiceField(choices=Pagamento.TIPOS_MODELO)
    pagamento_relacionado_id = serializers.IntegerField(write_only=True, required=False)
    numero_parcela = serializers.IntegerField(required=True)
    data_proximo_pagamento = serializers.DateField(required=False, allow_null=True)
    status_pagamento = serializers.ChoiceField(choices=Pagamento.STATUS_CHOICES, read_only=True)

    class Meta:
        model = Pagamento
        fields = [
            "id",
            "tipo_modelo",
            "pagamento_relacionado_id",
            "valor_pago",
            "data_pagamento",
            "data_proximo_pagamento",
            "numero_parcela",
            "status_pagamento",
            "gateway_pagamento",
            "transaction_id",
            "payment_method",
            "nome_cartao",
            "ultimos_digitos",
            "bandeira_cartao",
        ]

    def create(self, validated_data):
        from django.contrib.contenttypes.models import ContentType
        related_id = validated_data.pop("pagamento_relacionado_id", None)
        tipo_modelo = validated_data.get("tipo_modelo")
        model_map = {
            "planejamento": Planejamento,
            "inscricao": Inscricao,
        }
        model_cls = model_map.get(tipo_modelo)
        if model_cls and related_id:
            try:
                obj = model_cls.objects.get(id=related_id)
            except model_cls.DoesNotExist:
                raise serializers.ValidationError({"pagamento_relacionado_id": "Objeto relacionado não encontrado."})
            validated_data["content_type"] = ContentType.objects.get_for_model(model_cls)
            validated_data["object_id"] = obj.id
        return super().create(validated_data)


class LoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lote
        fields = [
            "id",
            "descricao",
            "valor_unitario",
            "unidades",
            "status",
        ]

