# Generated by Django 5.0.2 on 2024-02-26 14:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_autor"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="autor",
            options={"verbose_name_plural": "Autores"},
        ),
        migrations.CreateModel(
            name="Livro",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("titulo", models.CharField(blank=True, max_length=100, unique=True)),
                ("isbn", models.CharField(max_length=200)),
                ("quantidade", models.IntegerField()),
                ("preco", models.DecimalField(decimal_places=2, max_digits=6)),
                ("autores", models.ManyToManyField(related_name="livros", to="core.autor")),
                ("categoria", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="core.categoria")),
                ("editora", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="core.editora")),
            ],
        ),
    ]
