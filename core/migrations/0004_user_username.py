# Generated by Django 5.0.2 on 2024-02-26 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_editora"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="username",
            field=models.CharField(default="...", max_length=50, unique=True),
        ),
    ]
