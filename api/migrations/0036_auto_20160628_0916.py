# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0035_auto_20160627_1324'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='vlanmodel',
            unique_together=set([('switch', 'vlan_id')]),
        ),
    ]
