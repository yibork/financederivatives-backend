# Generated by Django 4.2.11 on 2024-05-17 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='linkedinurl',
            field=models.URLField(blank=True, max_length=255),
        ),
    ]