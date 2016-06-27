# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0034_auto_20160625_1635'),
    ]

    operations = [
        migrations.RenameField(
            model_name='switchmodel',
            old_name='logged_in_symbol',
            new_name='system_name',
        ),
    ]
