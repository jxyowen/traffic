# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20160621_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generatormodel',
            name='ip',
            field=models.GenericIPAddressField(),
        ),
    ]
