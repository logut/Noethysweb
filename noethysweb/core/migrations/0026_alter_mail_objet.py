# Generated by Django 3.2.9 on 2021-12-17 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_alter_modeleemail_objet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail',
            name='objet',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Objet'),
        ),
    ]