# Generated by Django 4.2.14 on 2024-09-13 18:00

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0014_alter_user_passage_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="itenscompra",
            name="preco",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name="user",
            name="passage_id",
            field=models.CharField(
                default=uuid.UUID("9bb221bc-eeaf-49de-9599-23c32719fbb6"), max_length=255, unique=True
            ),
        ),
    ]
