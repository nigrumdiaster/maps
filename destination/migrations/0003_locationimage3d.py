# Generated by Django 5.0.6 on 2024-07-17 09:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('destination', '0002_category_location_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationImage3D',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images3D', models.FileField(upload_to='images/location/3D')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images3D', to='destination.location')),
            ],
        ),
    ]