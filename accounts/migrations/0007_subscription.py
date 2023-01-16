# Generated by Django 4.1.3 on 2023-01-07 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0006_alter_user_type"),
    ]

    operations = [
        migrations.CreateModel(
            name="Subscription",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("type", models.CharField(max_length=50)),
                ("value", models.PositiveIntegerField()),
                ("details", models.TextField(blank=True, null=True)),
            ],
        ),
    ]
