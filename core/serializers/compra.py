from rest_framework.serializers import CharField, ModelSerializer, SerializerMethodField

from core.models import Compra, ItensCompra

class ItensCompraSerializer(ModelSerializer):
    total_itens = SerializerMethodField()

    def get_total_itens(self, instance):
        return instance.livro.preco * instance.quantidade
    class Meta:
        model = ItensCompra
        fields = ("livro", "quantidade", "total_itens")
        depth = 1
class CompraSerializer(ModelSerializer):
    usuario = CharField(source="user.email", read_only=True)
    status = CharField(source="get_status_display", read_only=True)
    itens = ItensCompraSerializer(many=True, read_only=True) 
    class Meta:
        model = Compra
        fields = ("id", "usuario", "status", "total", "itens")

class CriarEditarItensCompraSerializer(ModelSerializer):
    class Meta:
        model = ItensCompra
        fields = ("livro", "quantidade")

class CriarEditarCompraSerializer(ModelSerializer):
    itens = CriarEditarItensCompraSerializer(many=True) 
    class Meta:
        model = Compra
        fields = ("usuario", "itens")
    
    def create(self, validated_data):
        itens_data = validated_data.pop("itens")
        compra = Compra.objects.create(**validated_data)
        for item_data in itens_data:
            ItensCompra.objects.create(compra=compra, **item_data)
        compra.save()
        return compra