# Generated by Django 4.0.6 on 2024-04-19 05:54

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LeaveReasonModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('reason_en', models.CharField(blank=True, max_length=500, unique=True)),
                ('reason_kh', models.CharField(blank=True, max_length=500, unique=True)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'Leave Reason',
                'verbose_name_plural': 'Leave Reason',
                'db_table': 'ftb_eleave_leave_reason',
                'managed': True,
            },
        ),
    ]
