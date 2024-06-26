from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from .models import JobPage
from wagtail import hooks
from django.urls import path
from wagtail.admin.menu import MenuItem
from django.core.mail import send_mail
from django.conf import settings
import pandas as pd
from io import BytesIO
from django.core.mail import EmailMessage
from django.utils.html import format_html
from django.templatetags.static import static

class JobPageAdmin(ModelAdmin):
    model = JobPage
    menu_label = 'Jobs'  # Label in the admin menu
    menu_icon = 'folder-open-inverse'  # Icon from Wagtail or FontAwesome
    menu_order = 20  # Order in the admin menu
    add_to_settings_menu = False  # Show in 'Settings' menu
    exclude_from_explorer = False  # Show in 'Explorer' navigation
    list_display = ('job_title', 'company_name', 'location')
    search_fields = ('job_title', 'company_name__name', 'location__name')
    list_per_page = 10  # Number of jobs displayed per page

@hooks.register('after_create_page')
def send_notification(request, page):
    if isinstance(page, JobPage):
        # Fetch all jobs from the database
        data = list(JobPage.objects.all().values(
            'job_title', 'company_name__name', 'location__name', 'industry__name', 'categories__name', 
            'contract_type', 'duration', 'month', 'job_description', 'notes_feedbacks', 'language_requirements', 
            'expected_salary', 'currency__code', 'coding_languages__name', 'asset_class', 'interview_report_link', 
            'contact_persons__name', 'contact_persons__email', 'contact_persons__linkedin', 
            'contact_interns__name', 'contact_interns__email', 'contact_interns__linkedin'
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

modeladmin_register(JobPageAdmin)

@hooks.register('construct_main_menu')
def hide_images_menu_item(request, menu_items):
    menu_items[:] = [item for item in menu_items if item.name not in ['help', 'images', 'documents']]

@hooks.register('insert_global_admin_css')
def global_admin_css():
    return '<link rel="stylesheet" href="/static/css/custom_admin.css">'
@hooks.register('insert_editor_js')
def editor_js():
    js_files = [
        '/static/js/enable_new_company.js',  # Update this path
    ]
    js_includes = ''.join(['<script src="{}"></script>'.format(static(filename)) for filename in js_files])
    return js_includes

@hooks.register('insert_editor_css')
def custom_favicon():
    return format_html(
        '<link rel="icon" href="{}" type="image/x-icon">'
        '<link rel="shortcut icon" href="{}" type="image/x-icon">'
        '<link rel="apple-touch-icon" sizes="180x180" href="{}">'
        '<link rel="icon" type="image/png" sizes="32x32" href="{}">'
        '<link rel="icon" type="image/png" sizes="16x16" href="{}">',
        static('logo/logo192.png'),
        static('logo/logo192.png'),
        static('logo/logo192.png'),
        static('logo/logo192.png'),
        static('logo/logo192.png'),
    )

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
