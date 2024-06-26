# Generated by Django 4.2.11 on 2024-05-22 15:08

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('joblistings', '0010_alter_jobpage_job_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.RenameField(
            model_name='jobpage',
            old_name='coding_language',
            new_name='asset_class',
        ),
        migrations.RenameField(
            model_name='jobpage',
            old_name='contact_person_2_name',
            new_name='categories',
        ),
        migrations.RenameField(
            model_name='jobpage',
            old_name='contact_person_2_role',
            new_name='coding_languages',
        ),
        migrations.RenameField(
            model_name='jobpage',
            old_name='job_type',
            new_name='contract_type',
        ),
        migrations.RenameField(
            model_name='jobpage',
            old_name='contact_person_3_name',
            new_name='expected_salary',
        ),
        migrations.RenameField(
            model_name='jobpage',
            old_name='application_link_email',
            new_name='interview_report_link',
        ),
        migrations.RenameField(
            model_name='jobpage',
            old_name='benefits',
            new_name='job_description',
        ),
        migrations.RenameField(
            model_name='jobpage',
            old_name='contact_information',
            new_name='notes_feedbacks',
        ),
        migrations.RemoveField(
            model_name='jobpage',
            name='contact_person_1_linkedin',
        ),
        migrations.RemoveField(
            model_name='jobpage',
            name='contact_person_1_name',
        ),
        migrations.RemoveField(
            model_name='jobpage',
            name='contact_person_1_role',
        ),
        migrations.RemoveField(
            model_name='jobpage',
            name='contact_person_2_linkedin',
        ),
        migrations.RemoveField(
            model_name='jobpage',
            name='contact_person_3_linkedin',
        ),
        migrations.RemoveField(
            model_name='jobpage',
            name='contact_person_3_role',
        ),
        migrations.RemoveField(
            model_name='jobpage',
            name='department',
        ),
        migrations.RemoveField(
            model_name='jobpage',
            name='education_level',
        ),
        migrations.RemoveField(
            model_name='jobpage',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='jobpage',
            name='ex_current_intern_link',
        ),
        migrations.RemoveField(
            model_name='jobpage',
            name='ex_current_linkedin_link',
        ),
        migrations.RemoveField(
            model_name='jobpage',
            name='experience_level',
        ),
        migrations.RemoveField(
            model_name='jobpage',
            name='full_description',
        ),
        migrations.RemoveField(
            model_name='jobpage',
            name='how_to_apply',
        ),
        migrations.RemoveField(
            model_name='jobpage',
            name='job_company_description',
        ),
        migrations.RemoveField(
            model_name='jobpage',
            name='link_linkedin_offer',
        ),
        migrations.RemoveField(
            model_name='jobpage',
            name='mail_professional_1',
        ),
        migrations.RemoveField(
            model_name='jobpage',
            name='mail_professional_2',
        ),
        migrations.RemoveField(
            model_name='jobpage',
            name='mail_professional_3',
        ),
        migrations.RemoveField(
            model_name='jobpage',
            name='position',
        ),
        migrations.RemoveField(
            model_name='jobpage',
            name='post_date',
        ),
        migrations.RemoveField(
            model_name='jobpage',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='jobpage',
            name='remote_work',
        ),
        migrations.RemoveField(
            model_name='jobpage',
            name='responsibilities',
        ),
        migrations.RemoveField(
            model_name='jobpage',
            name='salary_range',
        ),
        migrations.RemoveField(
            model_name='jobpage',
            name='skills_required',
        ),
        migrations.RemoveField(
            model_name='jobpage',
            name='travel_requirements',
        ),
        migrations.RemoveField(
            model_name='jobpage',
            name='work_hours',
        ),
        migrations.AddField(
            model_name='jobpage',
            name='duration',
            field=models.IntegerField(blank=True, help_text='Duration in months', null=True),
        ),
        migrations.CreateModel(
            name='ContactPerson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('linkedin', models.URLField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('job_page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='contact_persons', to='joblistings.jobpage')),
            ],
        ),
        migrations.AlterField(
            model_name='jobpage',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='joblistings.city'),
        ),
    ]
