# Generated by Django 5.0.6 on 2024-07-24 02:23

import destination.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('destination', '0002_category_location_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='PanoramicImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paranomicimage', models.FileField(upload_to=destination.models.get_360image_upload_path)),
                ('location', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='paranomicimage', to='destination.location')),
            ],
        ),
    ]