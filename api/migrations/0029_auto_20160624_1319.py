# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_auto_20160624_1315'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vlanmodel',
            options={'ordering': ('vlan_id',)},
        ),
        migrations.AddField(
            model_name='vlanmodel',
            name='vlan_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
