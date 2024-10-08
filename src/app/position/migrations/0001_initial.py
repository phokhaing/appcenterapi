# Generated by Django 4.0.6 on 2024-04-19 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_en', models.CharField(blank=True, max_length=500, null=True)),
                ('name_kh', models.CharField(blank=True, max_length=500, null=True)),
                ('segment', models.CharField(blank=True, max_length=500, null=True)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('is_active', models.BooleanField(blank=True, default=True, null=True)),
            ],
            options={
                'verbose_name': 'Position',
                'verbose_name_plural': 'Positions',
                'db_table': 'ftb_position',
                'managed': True,
            },
        ),
    ]
