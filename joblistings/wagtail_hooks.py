# wagtail_hooks.py
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from .models import JobPage
from wagtail import hooks
#from .views import JobImportView
from django.urls import path
from wagtail.admin.menu import MenuItem
from django.core.mail import send_mail
from django.conf import settings
import pandas as pd
from io import BytesIO
from django.core.mail import EmailMessage


from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

class JobPageAdmin(ModelAdmin):
    model = JobPage
    menu_label = 'Jobs'  # Label in the admin menu
    menu_icon = 'folder-open-inverse'  # Icon from Wagtail or FontAwesome
    menu_order = 20  # Order in the admin menu
    add_to_settings_menu = False  # Show in 'Settings' menu
    exclude_from_explorer = False  # Show in 'Explorer' navigation
    list_display = ('job_title', 'company_name', 'location', 'post_date')
    search_fields = ('job_title', 'company_name', 'location')
    list_per_page = 10  # Number of jobs displayed per page

@hooks.register('after_create_page')
def send_notification(request, page):
    if isinstance(page, JobPage):
        # Fetch all jobs from the database
        data = list(JobPage.objects.all().values(
            'job_title', 'company_name', 'location', 'profile', 'job_type', 'industry', 
            'department', 'experience_level', 'education_level', 'skills_required', 'responsibilities', 
            'job_company_description', 'language_requirements', 'salary_range', 'benefits', 'work_hours',
            'remote_work', 'travel_requirements', 'full_description', 'contact_information', 
            'application_link_email', 'how_to_apply', 'post_date', 'start_date', 'ex_current_intern_link',
            'ex_current_linkedin_link', 'professional_1_name', 'contact_person_1_linkedin', 'mail_professional_1',
            'contact_person_2_name', 'contact_person_2_linkedin', 'contact_person_3_name', 
            'contact_person_3_linkedin', 'link_linkedin_offer'
        ))
        df = pd.DataFrame(data)

        # Create a BytesIO buffer for the Excel file
        excel_file = BytesIO()
        df.to_excel(excel_file, index=False, engine='openpyxl')
        excel_file.seek(0)  # Rewind the buffer

        # Email sending
        email = EmailMessage(
            subject='New Job Added',
            body=f'A new job titled "{page.job_title}" at "{page.company_name}" has been added.',
            from_email=settings.EMAIL_HOST_USER,
            to=['yassine.ibork123@gmail.com'],  # Change to your administrator's email
            attachments=[('JobList.xlsx', excel_file.read(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')]
        )

        email.send()
        print('Email with Excel file sent successfully!')

modeladmin_register(JobPageAdmin)



# # @hooks.register('register_admin_menu_item')
# # def register_excel_upload_menu_item():
# #     return MenuItem(
# #         'Upload Excel',
# #         '/admin/upload_excel/',
# #         classnames='icon icon-upload',
# #         order=1000
# #     )

#@hooks.register('register_admin_menu_item')
# def register_import_menu_item():
#     return MenuItem(
#         'Import Jobs',
#         '/admin/import-jobs/',
#         classnames='icon icon-download',
#         order=999
#     )

# @hooks.register('register_admin_urls')
# def register_admin_view():
#     return [
#         path('import-jobs/', JobImportView.as_view(), name='job_import'),
#     ]
