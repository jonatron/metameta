# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hondacar',
            options={'ordering': ['-created_at'], 'verbose_name': 'car'},
        ),
        migrations.AddField(
            model_name='basecar',
            name='created_at',
            field=models.DateTimeField(default=None, auto_now_add=True),
            preserve_default=False,
        ),
    ]
