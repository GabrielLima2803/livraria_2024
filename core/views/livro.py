from rest_framework.viewsets import ModelViewSet

from core.models import Livro
from core.serializers import LivroSerializer, LivroDetailSerializer, LivroListSerializer

from rest_framework.permissions import IsAuthenticated


class LivroViewSet(ModelViewSet):
    queryset = Livro.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == "list":
            return LivroListSerializer
        elif self.action == "retrieve":
            return LivroDetailSerializer
        return LivroSerializer