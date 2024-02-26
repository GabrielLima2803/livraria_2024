from django.db import models

class Autor(models.Model):
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Autores"

    def __str__(self):
        return self.nome