# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_auto_20160624_1010'),
    ]

    operations = [
        migrations.AddField(
            model_name='vlanmodel',
            name='traffic',
            field=models.CharField(default='Off', max_length=10, choices=[('Off', 'Off'), ('On', 'On')]),
        ),
    ]
