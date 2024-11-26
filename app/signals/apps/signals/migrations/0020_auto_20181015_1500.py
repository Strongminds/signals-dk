# SPDX-License-Identifier: MPL-2.0
# Copyright (C) 2018 - 2021 Gemeente Amsterdam
# Generated by Django 2.1.2 on 2018-10-15 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signals', '0019_auto_20181009_1321'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='department',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='maincategory',
            options={'ordering': ('name',), 'verbose_name_plural': 'Main Categories'},
        ),
        migrations.AlterModelOptions(
            name='signal',
            options={'ordering': ('created_at',)},
        ),
        migrations.AlterModelOptions(
            name='status',
            options={'get_latest_by': 'datetime',
                     'permissions': (
                         ('push_to_sigmax', 'Push to Sigmax/CityControl'),
                     ),
                     'verbose_name_plural': 'Statuses'},
        ),
        migrations.AlterModelOptions(
            name='subcategory',
            options={'ordering': ('name',), 'verbose_name_plural': 'Sub Categories'},
        ),
    ]
