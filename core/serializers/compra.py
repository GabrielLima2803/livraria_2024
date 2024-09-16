from rest_framework.serializers import (
    CharField,
    CurrentUserDefault,
    DateTimeField, 
    HiddenField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
)
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
    usuario = CharField(source="usuario.email", read_only=True)
    status = CharField(source="get_status_display", read_only=True)
    data = DateTimeField(read_only=True) 
    itens = ItensCompraSerializer(many=True, read_only=True)

    class Meta:
        model = Compra
        fields = ("id", "usuario", "status", "total", "data", "itens")


class CriarEditarItensCompraSerializer(ModelSerializer):
    
    class Meta:
        model = ItensCompra
        fields = ("livro", "quantidade")
    
    def validate(self, data):
        if data["quantidade"] > data["livro"].quantidade:
            raise ValidationError("Quantidade de itens maior do que a quantidade em estoque.")
        return data


class CriarEditarCompraSerializer(ModelSerializer):
    usuario = HiddenField(default=CurrentUserDefault())
    itens = CriarEditarItensCompraSerializer(many=True)

    class Meta:
        model = Compra
        fields = ("usuario", "itens")

    def create(self, validated_data):
        itens = validated_data.pop("itens")
        compra = Compra.objects.create(**validated_data)
        for item in itens:
            item["preco"] = item["livro"].preco
            ItensCompra.objects.create(compra=compra, **item)
        compra.save()
        return compra

    def update(self, instance, validated_data):
        itens = validated_data.pop("itens")
        if itens:
            instance.itens.all().delete()
            for item in itens:
                item["preco"] = item["livro"].preco 
                ItensCompra.objects.create(compra=instance, **item)
        instance.save()
        return super().update(instance, validated_data)
