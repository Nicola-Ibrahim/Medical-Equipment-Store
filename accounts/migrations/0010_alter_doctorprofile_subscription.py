# Generated by Django 4.1.3 on 2023-01-14 13:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0009_alter_doctorprofile_subscription"),
    ]

    operations = [
        migrations.AlterField(
            model_name="doctorprofile",
            name="subscription",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="accounts.subscription",
            ),
        ),
    ]