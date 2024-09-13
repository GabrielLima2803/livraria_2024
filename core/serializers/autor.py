from rest_framework.serializers import ModelSerializer

from core.models import Autor


class AutorSeralizer(ModelSerializer):
    class Meta:
        model = Autor
        fields = "__all__"
