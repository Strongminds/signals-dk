# SPDX-License-Identifier: MPL-2.0
# Copyright (C) 2022 Gemeente Amsterdam
# Generated by Django 3.2.13 on 2022-06-10 07:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signals', '0159_location_area_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeletedSignal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signal_id', models.PositiveBigIntegerField(editable=False)),
                ('signal_uuid', models.UUIDField(editable=False)),
                ('parent_signal_id', models.PositiveBigIntegerField(blank=True, editable=False, null=True)),
                ('signal_state', models.CharField(blank=True, choices=[
                    ('m', 'Gemeld'),
                    ('i', 'In afwachting van behandeling'),
                    ('b', 'In behandeling'),
                    ('h', 'On hold'),
                    ('ingepland', 'Ingepland'),
                    ('ready to send', 'Extern: te verzenden'),
                    ('o', 'Afgehandeld'),
                    ('a', 'Geannuleerd'),
                    ('reopened', 'Heropend'),
                    ('s', 'Gesplitst'),
                    ('closure requested', 'Extern: verzoek tot afhandeling'),
                    ('reaction requested', 'Reactie gevraagd'),
                    ('reaction received', 'Reactie ontvangen'),
                    ('sent', 'Extern: verzonden'),
                    ('send failed', 'Extern: mislukt'),
                    ('done external', 'Extern: afgehandeld'),
                    ('reopen requested', 'Verzoek tot heropenen')
                ], editable=False, max_length=20)),
                ('signal_state_set_at', models.DateTimeField(editable=False)),
                ('signal_created_at', models.DateTimeField(editable=False)),
                ('deleted_by', models.EmailField(blank=True, editable=False, max_length=254, null=True)),
                ('deleted_at', models.DateTimeField(auto_now_add=True)),
                ('batch_uuid', models.UUIDField(blank=True, editable=False, null=True)),
                ('action', models.CharField(choices=[('automatic', 'Automatic'), ('manual', 'Manual')],
                                            editable=False, max_length=12)),
                ('note', models.TextField(blank=True, editable=False, null=True)),
                ('category', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.DO_NOTHING,
                                               related_name='+', to='signals.category')),
            ],
        ),
    ]
