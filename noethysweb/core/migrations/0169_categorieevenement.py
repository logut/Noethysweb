# Generated by Django 3.2.21 on 2024-11-10 22:36

import core.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0168_auto_20241109_1833'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategorieEvenement',
            fields=[
                ('idcategorie', models.AutoField(db_column='IDcategorie', primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200, verbose_name='Nom')),
                ('image', models.ImageField(blank=True, null=True, upload_to=core.models.get_uuid_path, verbose_name='Image')),
                ('limitations', models.CharField(blank=True, choices=[(None, 'Aucune'), ('1EVTSEMAINE', '1 événement par semaine max'), ('2EVTSEMAINE', '2 événements par semaine max'), ('3EVTSEMAINE', '3 événements par semaine max')], default=None, max_length=100, null=True, verbose_name='Limitation')),
                ('activite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.activite', verbose_name='Activité')),
            ],
            options={
                'verbose_name': "catégorie d'événement",
                'verbose_name_plural': "catégories d'événements",
                'db_table': 'evenements_categories',
            },
        ),
    ]