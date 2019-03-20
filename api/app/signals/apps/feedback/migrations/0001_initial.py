# Generated by Django 2.1.7 on 2019-03-20 13:40

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('signals', '0039_auto_20190320_1436'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, primary_key=True, serialize=False)),
                ('requested_before', models.DateTimeField(editable=False)),
                ('is_satisfied', models.BooleanField(null=True)),
                ('allows_contact', models.BooleanField(default=False)),
                ('text', models.TextField(blank=True, max_length=1000, null=True)),
                ('_signal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedback', to='signals.Signal')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StandardAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_visible', models.BooleanField(default=True)),
                ('is_satisfied', models.BooleanField(default=True)),
                ('text', models.TextField(max_length=1000)),
            ],
        ),
    ]
