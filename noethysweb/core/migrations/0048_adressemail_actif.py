# Generated by Django 3.2.11 on 2022-10-23 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0047_auto_20221012_2120'),
    ]

    operations = [
        migrations.AddField(
            model_name='adressemail',
            name='actif',
            field=models.BooleanField(default=True, help_text='Décochez la case pour désactiver cette adresse.', verbose_name='Actif'),
        ),
    ]