# Generated by Django 4.1.3 on 2023-01-08 18:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0008_deliveryworkerprofile_subscription_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="doctorprofile",
            name="subscription",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="users",
                to="accounts.subscription",
            ),
        ),
    ]
