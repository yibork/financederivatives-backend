# Generated by Django 4.2.11 on 2024-05-23 19:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('joblistings', '0020_rename_month_jobpage_start_month'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3, unique=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='jobpage',
            name='start_month',
        ),
        migrations.AddField(
            model_name='jobpage',
            name='month',
            field=models.CharField(blank=True, choices=[('01', 'January'), ('02', 'February'), ('03', 'March'), ('04', 'April'), ('05', 'May'), ('06', 'June'), ('07', 'July'), ('08', 'August'), ('09', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')], max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='jobpage',
            name='new_currency_code',
            field=models.CharField(blank=True, help_text='Currency code (e.g., USD)', max_length=3),
        ),
        migrations.AddField(
            model_name='jobpage',
            name='new_currency_name',
            field=models.CharField(blank=True, help_text='Currency name (e.g., United States Dollar)', max_length=255),
        ),
        migrations.AddField(
            model_name='jobpage',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='jobs', to='joblistings.currency'),
        ),
    ]
