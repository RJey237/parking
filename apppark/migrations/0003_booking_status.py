# Generated by Django 5.1.7 on 2025-04-05 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apppark', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('booked', 'Booked'), ('arrived', 'Arrived'), ('left', 'Left'), ('rejected', 'Rejected')], default='booked', max_length=100),
        ),
    ]
