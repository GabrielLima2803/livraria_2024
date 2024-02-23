from rest_framework.serializers import ModelSerializer

from core.models import Categoria

class CategoriaSeralizer(ModelSerializer):
    class Meta:
        model = Categoria
        fields = "__all__"