# Generated by Django 4.2.11 on 2024-05-23 19:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('joblistings', '0018_contactintern'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='jobpage',
            name='start_date',
        ),
        migrations.AddField(
            model_name='jobpage',
            name='month',
            field=models.CharField(blank=True, choices=[('01', 'January'), ('02', 'February'), ('03', 'March'), ('04', 'April'), ('05', 'May'), ('06', 'June'), ('07', 'July'), ('08', 'August'), ('09', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')], max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='jobpage',
            name='new_category_name',
            field=models.CharField(blank=True, help_text="Add a new category if it's not listed", max_length=255),
        ),
        migrations.AddField(
            model_name='jobpage',
            name='new_industry_name',
            field=models.CharField(blank=True, help_text="Add a new industry if it's not listed", max_length=255),
        ),
        migrations.AlterField(
            model_name='jobpage',
            name='categories',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='joblistings.category'),
        ),
        migrations.AlterField(
            model_name='jobpage',
            name='industry',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='joblistings.industry'),
        ),
    ]