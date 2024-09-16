from django.db import models
from django.db import transaction

from .livro import Livro
from .user import User

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class Compra(models.Model):
    class StatusCompra(models.IntegerChoices):
        CARRINHO = 1, "Carrinho"
        REALIZADO = 2, "Realizado"
        PAGO = 3, "Pago"
        ENTREGUE = 4, "Entregue"
    class TipoPagamento(models.IntegerChoices):
        CARTAO_CREDITO = 1, "Cartão de Crédito"
        CARTAO_DEBITO = 2, "Cartão de Débito"
        PIX = 3, "PIX"
        BOLETO = 4, "Boleto"
        TRANSFERENCIA_BANCARIA = 5, "Transferência Bancária"
        DINHEIRO = 6, "Dinheiro"
        OUTRO = 7, "Outro"

    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name="compras")
    status = models.IntegerField(choices=StatusCompra.choices, default=StatusCompra.CARRINHO)
    tipo_pagamento = models.IntegerField(choices=TipoPagamento.choices, default=TipoPagamento.CARTAO_CREDITO)
    data = models.DateTimeField(auto_now_add=True)


    @property
    def total(self):
        return sum(item.preco * item.quantidade for item in self.itens.all())
    
    # @action(detail=True, methods=["POST"], url_path="finalizar")
    # def finalizar(self, request, pk=None):
    #     compra = self.get_object()
    #     if compra.status != Compra.StatusCompra.CARRINHO:
    #         return Response(
    #             status=status.HTTP_400_BAD_REQUEST,
    #             data={"status": "Compra já finalizada"},
    #         )
    #     with transaction.atomic():
    #         for item in compra.itens.all():
    #             if item.quantidade > item.livro.quantidade:
    #                 return Response(
    #                     status=status.HTTP_400_BAD_REQUEST,
    #                     data={
    #                         "status": "Quantidade insuficiente",
    #                         "livro": item.livro.titulo,
    #                     },                    
    #                 )
    #             item.livro.quantidade -= item.quantidade 
    #             item.livro.save()
    #         compra.status = Compra.StatusCompra.REALIZADO
    #         compra.save()
    #     return Response(status=status.HTTP_200_OK, data={"status": "Compra finalizada"})


class ItensCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name="itens")
    livro = models.ForeignKey(Livro, on_delete=models.PROTECT, related_name="+")
    quantidade = models.IntegerField(default=1)
    preco = models.DecimalField(max_digits=10, decimal_places=2, default=0)