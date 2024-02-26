from django.db import models
from core.models import Autor, Categoria, Editora

class Livro(models.Model):
    titulo = models.CharField(max_length=100, blank=True, unique=True)
    isbn = models.CharField(max_length=200)
    quantidade = models.IntegerField()
    preco = models.DecimalField(decimal_places=2, max_digits=6)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    editora = models.ForeignKey(Editora, on_delete=models.PROTECT)
    autores = models.ManyToManyField(Autor, related_name="livros")



    def __str__(self):
        return f"{self.titulo}  R$({self.preco})"
