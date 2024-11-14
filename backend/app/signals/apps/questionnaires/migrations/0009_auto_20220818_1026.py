# SPDX-License-Identifier: MPL-2.0
# Copyright (C) 2022 Gemeente Amsterdam
# Generated by Django 3.2.15 on 2022-08-18 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaires', '0008_auto_20220329_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='field_type',
            field=models.CharField(choices=[('boolean', 'Boolean'),
                                            ('date', 'Date'),
                                            ('date_time', 'DateTime'),
                                            ('dutch_telephone_number', 'Telephone number (NL)'),
                                            ('email', 'Email'),
                                            ('float', 'Float'),
                                            ('image', 'Image'),
                                            ('integer', 'Integer'),
                                            ('plain_text', 'PlainText'),
                                            ('positive_integer', 'PositiveInteger'),
                                            ('selected_object', 'Selected object'),
                                            ('time', 'Time')], max_length=255),
        ),
    ]
