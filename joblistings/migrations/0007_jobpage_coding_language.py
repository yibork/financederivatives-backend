# Generated by Django 4.2.11 on 2024-05-05 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('joblistings', '0006_jobpage_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobpage',
            name='coding_language',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
