# Generated by Django 4.0.6 on 2024-04-19 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LeaveFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload_file_name', models.CharField(blank=True, max_length=500, null=True)),
                ('original_name', models.CharField(blank=True, max_length=500, null=True)),
                ('file_type', models.CharField(blank=True, max_length=255, null=True)),
                ('extension', models.CharField(blank=True, max_length=12, null=True)),
                ('file_size', models.CharField(blank=True, max_length=255, null=True)),
                ('timestamp', models.IntegerField(blank=True, null=True)),
                ('file_path', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('status', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Leave file',
                'verbose_name_plural': 'Leave files',
                'db_table': 'ftb_eleave_leave_file',
                'managed': True,
            },
        ),
    ]
