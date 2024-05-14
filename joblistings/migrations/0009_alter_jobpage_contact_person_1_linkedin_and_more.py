# Generated by Django 4.2.11 on 2024-05-14 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('joblistings', '0008_alter_jobpage_remote_work'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobpage',
            name='contact_person_1_linkedin',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='jobpage',
            name='contact_person_1_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='jobpage',
            name='contact_person_1_role',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]