from django.core.management.base import BaseCommand, CommandError
from openpyxl import load_workbook
from django.core.exceptions import ObjectDoesNotExist
from wagtail.models import Site
from joblistings.models import JobPage, JobIndexPage
import datetime

class Command(BaseCommand):
    help = 'Import jobs from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The path to the Excel file')

    def handle(self, *args, **options):
        file_path = options['file_path']
        wb = load_workbook(filename=file_path)
        ws = wb.active

        # Ensure that there is a JobIndexPage
        try:
            job_index_page = JobIndexPage.objects.live().first()
            if not job_index_page:
                raise ObjectDoesNotExist("Job Index Page does not exist.")
        except ObjectDoesNotExist:
            job_index_page = self.create_job_index_page()
            self.stdout.write(self.style.SUCCESS('Job Index Page created successfully.'))

        # Import jobs
        for row_index, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
            # Unpack all the row values
            (job_title, company_name, location, profile, job_type, industry, department,
             experience_level, education_level, skills_required, responsibilities,
             job_company_description, language_requirements, salary_range, benefits,
             work_hours, remote_work, travel_requirements, full_description,
             contact_information, application_link_email, how_to_apply,
             post_date, start_date, *rest) = row

            # Ensure that the mandatory fields are not empty (for example, job_title)
            if not job_title:  
                self.stdout.write(self.style.WARNING(f'Skipping job with empty title at row {row_index}'))
                continue

            # Prepare the job page data dictionary
            job_page_data = {
                'title': job_title.strip() if job_title else "No Title",
                'job_title': job_title,
                'company_name': company_name,
                'location': location,
                'profile': profile,
                'job_type': job_type,
                'industry': industry,
                'department': department,
                'experience_level': experience_level,
                'education_level': education_level,
                'skills_required': skills_required,
                'responsibilities': responsibilities,
                'job_company_description': job_company_description,
                'language_requirements': language_requirements,
                'salary_range': salary_range,
                'benefits': benefits,
                'work_hours': work_hours,
                'remote_work': remote_work,
                'travel_requirements': travel_requirements,
                'full_description': full_description,
                'contact_information': contact_information,
                'application_link_email': application_link_email,
                'how_to_apply': how_to_apply,
                'post_date': self.parse_date(post_date),
                'start_date': self.parse_date(start_date),
                # ... add other fields as necessary ...
            }

            try:
                job_page = JobPage(**job_page_data)
                job_index_page.add_child(instance=job_page)
                job_page.save_revision().publish()
                self.stdout.write(self.style.SUCCESS(f'Job "{job_title}" imported successfully at row {row_index}.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error saving job "{job_title}" at row {row_index}: {e}'))

    def create_job_index_page(self):
        root = Site.objects.get(is_default_site=True).root_page
        job_index_page = JobIndexPage(title="Main Job Listings")
        root.add_child(instance=job_index_page)
        job_index_page.save_revision().publish()
        return job_index_page
    
    def parse_date(self, date_string):
        """
        Parse the date from the format in the Excel sheet to a Python date object.
        You may need to adjust the parsing depending on the date format.
        """
        if date_string:
            try:
                return datetime.datetime.strptime(date_string, '%m/%d/%Y').date()
            except ValueError:
                self.stdout.write(self.style.WARNING(f'Invalid date format: {date_string}'))
        return None
