# Generated by Django 5.0.2 on 2024-03-11 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_alter_autor_options_livro"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="categoria",
            name="nome",
        ),
    ]