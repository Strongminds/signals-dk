# SPDX-License-Identifier: MPL-2.0
# Copyright (C) 2021 Gemeente Amsterdam
# Generated by Django 3.2.5 on 2021-12-01 11:51
from django.db import migrations, models

signal_filter_view_reverse_sql = 'DROP VIEW IF EXISTS "signals_filter_view";'

signal_filter_view_sql = f"""
{signal_filter_view_reverse_sql}
CREATE VIEW "signals_filter_view" AS
SELECT
       "s"."id" AS "signal_id",
       "s"."text",
       "s"."text_extra",
       "s"."source",
       "s"."created_at",
       "s"."updated_at",
       "s"."incident_date_start",
       "s"."incident_date_end",
       "s"."directing_departments_assignment_id",
       "s"."routing_assignment_id",
       CASE
           WHEN "s"."parent_id" IS NULL and "scs"."updated_at" IS NULL THEN True
           ELSE False
        END AS "is_signal",
       CASE
           WHEN "scs"."updated_at" IS NOT NULL THEN True
           ELSE False
        END AS "is_parent",
       CASE
           WHEN "scs"."updated_at" IS NOT NULL AND "scs"."updated_at" > "s"."updated_at" THEN True
           ELSE False
        END AS "has_changed_children",
       CASE
           WHEN "s"."parent_id" IS NOT NULL THEN True
           ELSE False
        END AS "is_child",
       "cp"."id" AS "parent_category_id",
       "cp"."slug" AS "parent_category_slug",
       "cp"."name" AS "parent_category_name",
       "c"."id" AS "child_category_id",
       "c"."slug" AS "child_category_slug",
       "c"."name" AS "child_category_name",
       "sc"."id" AS "category_assignment_id",
       "sc"."deadline" AS "category_assignment_deadline",
       "sc"."deadline_factor_3" AS "category_assignment_deadline_factor_3",
       "ss"."state" AS "status_state",
       "sp"."priority" AS "priority_priority",
       "sl"."buurt_code" AS "location_buurt_code",
       "sl"."address_text" AS "location_address_text",
       "sl"."area_code" AS "location_area_code",
       "sl"."area_type_code" AS "location_area_code_type",
       "sl"."stadsdeel" AS "location_stadsdeel",
       "sr"."email" AS "reporter_email",
       "sr"."phone" AS "reporter_phone",
       "st"."name" AS "type_name",
       "st"."created_by" AS "type_created_by",
       "st"."created_at" AS "type_created_at",
       "au"."email" AS "assigned_user_email",
       "ff"."is_satisfied" as "feedback_is_satisfied",
       "ff"."created_at" as "feedback_created_at",
       "ff"."submitted_at" as "feedback_submitted_at"
FROM "signals_signal" AS "s"
LEFT JOIN (
    SELECT MAX("inner_select"."updated_at") AS "updated_at", "inner_select"."parent_id"
    FROM "signals_signal" AS "inner_select"
    WHERE "inner_select"."parent_id" IS NOT NULL
    GROUP BY "inner_select"."parent_id"
) "scs" ON "scs"."parent_id" = "s"."id"
INNER JOIN "signals_categoryassignment" AS "sc" ON "s"."category_assignment_id" = "sc"."id"
INNER JOIN "signals_category" AS "c" ON "sc"."category_id" = "c"."id"
INNER JOIN "signals_category" AS "cp" ON "c"."parent_id" = "cp"."id"
INNER JOIN "signals_status" AS "ss" ON "s"."status_id" = "ss"."id"
INNER JOIN "signals_priority" AS "sp" ON "s"."priority_id" = "sp"."id"
INNER JOIN "signals_location" AS "sl" ON "s"."location_id" = "sl"."id"
LEFT JOIN "signals_reporter" AS "sr" ON "s"."reporter_id" = "sr"."id"
INNER JOIN "signals_type" AS "st" ON "s"."type_assignment_id" = "st"."id"
LEFT JOIN "signals_signaluser" AS "ss2" ON "s"."user_assignment_id" = "ss2"."id"
LEFT JOIN "auth_user" AS "au" ON "ss2"."user_id" = "au"."id"
LEFT JOIN (
    SELECT DISTINCT ON ("inner_select"."_signal_id") _signal_id,
                    "inner_select"."is_satisfied",
                    "inner_select"."created_at",
                    "inner_select"."submitted_at"
    FROM "feedback_feedback" AS "inner_select"
    ORDER BY "inner_select"."_signal_id" DESC, "inner_select"."created_at" DESC
) AS "ff" on "ff"."_signal_id" = "s"."id";
"""


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.RunSQL(sql=signal_filter_view_sql, reverse_sql=signal_filter_view_reverse_sql),
        migrations.CreateModel(
            name='SignalFilterView',
            fields=[
                ('signal_id', models.IntegerField(primary_key=True, serialize=False)),
                ('source', models.CharField(max_length=128)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('incident_date_start', models.DateTimeField()),
                ('is_signal', models.BooleanField()),
                ('is_parent', models.BooleanField()),
                ('has_changed_children', models.BooleanField()),
                ('is_child', models.BooleanField()),
                ('parent_category_id', models.IntegerField()),
                ('parent_category_slug', models.CharField(max_length=50)),
                ('child_category_id', models.IntegerField()),
                ('child_category_slug', models.CharField(max_length=50)),
                ('category_assignment_deadline', models.DateTimeField()),
                ('category_assignment_deadline_factor_3', models.DateTimeField()),
                ('status_state', models.CharField(blank=True, choices=[
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
                ], max_length=20)),
                ('priority_priority', models.CharField(max_length=10)),
                ('location_buurt_code', models.CharField(max_length=4)),
                ('location_address_text', models.CharField(max_length=255)),
                ('location_area_code', models.CharField(max_length=255)),
                ('location_area_code_type', models.CharField(max_length=255)),
                ('location_stadsdeel', models.CharField(max_length=1)),
                ('reporter_email', models.CharField(max_length=254)),
                ('reporter_phone', models.CharField(max_length=17)),
                ('type_name', models.CharField(max_length=3)),
                ('assigned_user_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('feedback_is_satisfied', models.BooleanField()),
                ('feedback_created_at', models.DateTimeField(blank=True, null=True)),
                ('feedback_submitted_at', models.DateTimeField(blank=True, null=True)),
                ('text', models.TextField()),
                ('text_extra', models.TextField(blank=True, null=True)),
                ('incident_date_end', models.DateTimeField()),
                ('parent_category_name', models.CharField(max_length=255)),
                ('child_category_name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'signals_filter_view',
                'managed': False,
            },
        ),
    ]
