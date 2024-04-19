# Generated by Django 4.0.6 on 2024-04-19 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LeaveRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staff_id', models.CharField(blank=True, max_length=255, null=True)),
                ('staff_name', models.CharField(blank=True, max_length=255, null=True)),
                ('staff_position', models.CharField(blank=True, max_length=255, null=True)),
                ('staff_department', models.CharField(blank=True, max_length=255, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('duration', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('from_time', models.CharField(blank=True, max_length=255, null=True)),
                ('to_time', models.CharField(blank=True, max_length=255, null=True)),
                ('hours', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('minute', models.IntegerField(blank=True, null=True)),
                ('total_time', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('reason', models.TextField(blank=True, null=True)),
                ('requested_at', models.DateTimeField(blank=True, null=True)),
                ('certifier_at', models.DateTimeField(blank=True, null=True)),
                ('authorizer_at', models.DateTimeField(blank=True, null=True)),
                ('rejected_at', models.DateTimeField(blank=True, null=True)),
                ('rejected_reason', models.TextField(blank=True, null=True)),
                ('canceled_at', models.DateTimeField(blank=True, null=True)),
                ('canceled_reason', models.TextField(blank=True, null=True)),
                ('incharge_request', models.CharField(blank=True, max_length=5, null=True)),
                ('incharge_certifier', models.CharField(blank=True, max_length=5, null=True)),
                ('incharge_authorizer', models.CharField(blank=True, max_length=5, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Leave request',
                'verbose_name_plural': 'Leave request',
                'db_table': 'ftb_eleave_leave_request',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='LeaveRequestStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Leave status',
                'verbose_name_plural': 'Leave status',
                'db_table': 'ftb_eleave_leave_status',
                'managed': True,
            },
        ),
    ]
