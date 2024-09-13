from rest_framework.viewsets import ModelViewSet

from core.models import Autor
from core.serializers import AutorSeralizer


class AutorViewSet(ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSeralizer
