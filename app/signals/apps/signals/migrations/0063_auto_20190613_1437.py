# SPDX-License-Identifier: MPL-2.0
# Copyright (C) 2019 - 2021 Gemeente Amsterdam
# Generated by Django 2.1.9 on 2019-06-13 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signals', '0062_rename_to_straatverlichting'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='statusmessagetemplate',
            options={
                'ordering': (
                    'category',
                    'state',
                    'order'
                ),
                'permissions': (
                    ('sia_statusmessagetemplate_write', 'Can write StatusMessageTemplates to SIA'),
                ),
                'verbose_name': 'Standaard afmeldtekst',
                'verbose_name_plural': 'Standaard afmeldteksten'
            },
        ),
    ]
