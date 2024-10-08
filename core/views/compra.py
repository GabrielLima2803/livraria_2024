from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from core.models import Compra
from core.serializers import CompraSerializer, CriarEditarCompraSerializer

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

class CompraViewSet(ModelViewSet):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer
    # permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ("create", "update"):
            return CriarEditarCompraSerializer
        return CompraSerializer

    def get_queryset(self):
        usuario = self.request.user
        if usuario.is_superuser:
            return Compra.objects.all()
        if usuario.groups.filter(name="Administradores"):
            return Compra.objects.all()
        return Compra.objects.filter(usuario=usuario)
    
    @action(detail=True, methods=["POST"])
    def finalizar(self, request, pk=None):
        compra = self.get_object()
        if compra.status != Compra.StatusCompra.CARRINHO:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"status": "Compra já finalizada"},
            )
        with transaction.atomic():
            for item in compra.itens.all():
                if item.quantidade > item.livro.quantidade:
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={
                            "status": "Quantidade insuficiente",
                            "livro": item.livro.titulo,
                        },                    
                    )
                item.livro.quantidade -= item.quantidade 
                item.livro.save()
            compra.status = Compra.StatusCompra.REALIZADO
            compra.save()
        return Response(status=status.HTTP_200_OK, data={"status": "Compra finalizada"})