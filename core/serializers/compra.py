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

