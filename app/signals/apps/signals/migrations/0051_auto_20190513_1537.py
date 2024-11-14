# SPDX-License-Identifier: MPL-2.0
# Copyright (C) 2019 - 2021 Gemeente Amsterdam
# Generated by Django 2.1.7 on 2019-05-13 13:37

from django.db import migrations

# as of now sub slugs are still unique, hence no main slugs below
TO_TRANSLATE = [
    ('bedrijfsafval', 'overig-afval'),
    ('stank-horecabedrijven', 'stankoverlast'),
    ('deelfiets', 'overig-openbare-ruimte'),
    ('overlast-op-het-water-vaargedrag', 'scheepvaart-nautisch-toezicht'),
    ('personen-op-het-water', 'overig-boten'),
    ('vuurwerkoverlast', 'overlast-door-afsteken-vuurwerk'),
    ('straatverlichting-openbare-klok', 'lantaarnpaal-straatverlichting'),
    ('verkeersoverlast-verkeerssituaties', 'verkeersoverlast'),
]
MESSAGE = 'Omdat er nieuwe categorieën zijn ingevoerd in SIA is deze melding overnieuw ingedeeld.'


def add_category_translations(apps, schema_editor):
    Category = apps.get_model('signals', 'Category')
    CategoryTranslation = apps.get_model('signals', 'CategoryTranslation')

    for from_slug, to_slug in TO_TRANSLATE:
        from_cat = Category.objects.get(slug=from_slug)
        to_cat = Category.objects.get(slug=to_slug)

        CategoryTranslation.objects.create(
            created_by=None,
            text=MESSAGE,
            old_category=from_cat,
            new_category=to_cat,
        )


class Migration(migrations.Migration):

    dependencies = [
        ('signals', '0050_merge_20190513_1348'),
    ]

    operations = [
        migrations.RunPython(add_category_translations),
    ]
