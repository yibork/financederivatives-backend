# Generated by Django 4.2.11 on 2024-05-22 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('joblistings', '0015_jobpage_new_company_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobpage',
            name='new_city_name',
            field=models.CharField(blank=True, help_text="Add a new city if it's not listed", max_length=255),
        ),
    ]