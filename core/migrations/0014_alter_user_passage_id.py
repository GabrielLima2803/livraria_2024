# Generated by Django 4.2.14 on 2024-09-13 17:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0013_itenscompra"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="passage_id",
            field=models.CharField(
                default=uuid.UUID("1e55ec67-28b0-482b-ab60-9acf22e47fdc"), max_length=255, unique=True
            ),
        ),
    ]
