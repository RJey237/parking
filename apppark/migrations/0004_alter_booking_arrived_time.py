# Generated by Django 5.1.7 on 2025-04-05 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apppark', '0003_booking_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='arrived_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
