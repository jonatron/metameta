# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseCar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('colour', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='FordCar',
            fields=[
                ('basecar_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cars.BaseCar')),
                ('horsepowers', models.IntegerField()),
            ],
            bases=('cars.basecar',),
        ),
        migrations.CreateModel(
            name='HondaCar',
            fields=[
                ('basecar_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cars.BaseCar')),
                ('cupholders', models.IntegerField()),
            ],
            bases=('cars.basecar',),
        ),
    ]
