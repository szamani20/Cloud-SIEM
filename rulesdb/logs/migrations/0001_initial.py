# Generated by Django 5.0.6 on 2024-07-15 19:10

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('log_id', models.AutoField(primary_key=True, serialize=False)),
                ('log_content', models.JSONField()),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('update_time', models.DateTimeField(blank=True, null=True)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='organization.organization')),
            ],
            options={
                'db_table': 'logs',
            },
        ),
    ]
