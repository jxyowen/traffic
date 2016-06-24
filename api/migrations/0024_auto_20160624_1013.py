# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_vlanmodel_traffic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vlanmodel',
            name='traffic',
            field=models.CharField(max_length=10, choices=[('Off', 'Off'), ('On', 'On')]),
        ),
    ]
