# Generated by Django 5.0.6 on 2024-07-03 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journey', '0002_journey_locations'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='journey',
            name='sound_url',
        ),
        migrations.AddField(
            model_name='journey',
            name='sound',
            field=models.FileField(blank=True, null=True, upload_to='sounds/journey/'),
        ),
    ]
