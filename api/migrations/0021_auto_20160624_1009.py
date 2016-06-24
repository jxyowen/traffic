# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_vlanmodel_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vlanmodel',
            name='status',
            field=models.CharField(max_length=10, choices=[('Idle', 'Idle'), ('Used', 'Used')]),
        ),
    ]
