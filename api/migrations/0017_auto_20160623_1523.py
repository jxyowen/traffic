# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_remove_generatormodel_tx_rate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='generatormodel',
            old_name='port',
            new_name='port_in_use',
        ),
    ]
