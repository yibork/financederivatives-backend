# views.py
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView
from wagtail.admin.messages import success, error
from .forms import JobImportForm
from .models import JobPage, JobIndexPage
from openpyxl import load_workbook
from rest_framework.generics import ListAPIView
from .serializers import JobPageSerializer
import os
from django.http import JsonResponse
from django.views import View
from django.core.management import call_command
from django.core.files.storage import default_storage
from rest_framework import viewsets

# joblistings/views.py

from django.http import JsonResponse
import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
import uuid
from django.contrib.auth.decorators import login_required

# Configure your Google Cloud credentials
dir_path = os.path.dirname(os.path.realpath(__file__))
SERVICE_ACCOUNT_FILE =  os.path.join(dir_path, 'secret', 'dashboard-finance-derivatives-0b16f2f20dc3.json')
SCOPES = ['https://www.googleapis.com/auth/jobs']
print("Attempting to load credentials from:", SERVICE_ACCOUNT_FILE)
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

client_service = build('jobs', 'v3', credentials=credentials)
project_id = 'projects/dashboard-finance-derivatives'

def job_search(request):
    # Hardcoding the job type in the query
    search_term = 'Engineer'  # Default to 'Engineer' if not specified
    job_categories = ['COMPUTER_AND_IT']  # Example category, adjust as necessary

    request_metadata = {
        'domain': 'example.com',
        'session_id': 'session123',
        'user_id': 'user123'
    }

    job_query = {
        'query': search_term,
        'jobCategories': job_categories  # Use jobCategories instead of jobType
    }

    body = {
        'searchMode': 'JOB_SEARCH',
        'requestMetadata': request_metadata,
        'jobQuery': job_query,
        'jobView': 'JOB_VIEW_FULL',
        'pageSize': 20
    }

    response = client_service.projects().jobs().search(
        parent=project_id, body=body).execute()

    jobs = response.get('matchingJobs', [])
    print(jobs)
    if not jobs:
        return JsonResponse({'message': 'No Job Results'}, status=404)

    results = [{
        'title': job.get('job', {}).get('title'),
        'description': job.get('job', {}).get('description')
    } for job in jobs]

    return JsonResponse({'jobs': results})
class ExcelUploadView(View):
    def get(self, request, *args, **kwargs):
        # Render the upload form template
        return render(request, 'admin/excel_upload_form.html')

    def post(self, request, *args, **kwargs):
        excel_file = request.FILES.get('excel_file')
        if not excel_file:
            return JsonResponse({'error': 'No file uploaded.'}, status=400)

        file_path = default_storage.save('tmp/excel_file.xlsx', excel_file)
        full_file_path = default_storage.path(file_path)

        try:
            # Call your management command here
            call_command('import_jobs', full_file_path)
            return JsonResponse({'success': 'Jobs imported successfully.'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        finally:
            # Clean up the file after import
            os.remove(full_file_path)

class JobImportView(FormView):
    template_name = 'job_import.html'
    form_class = JobImportForm
    success_url = reverse_lazy('wagtailadmin_home')  # Redirect to Wagtail admin home

    def form_valid(self, form):
        try:
            excel_file = form.cleaned_data['excel_file']
            wb = load_workbook(filename=excel_file)
            ws = wb.active
            job_index_page = JobIndexPage.objects.live().first()

            if not job_index_page:
                return error(self.request, "Job Index Page does not exist.")

            for row in ws.iter_rows(min_row=2, values_only=True):
                job_page_data = {
                    'title': row[0],
                    'job_title': row[0],
                    'company_name': row[1],
                    'location': row[2],
                    # ... other fields ...
                }
                job_page = JobPage(**job_page_data)
                job_index_page.add_child(instance=job_page)
                job_page.save_revision().publish()

            success(self.request, "Jobs imported successfully.")
        except Exception as e:
            error(self.request, f"An error occurred: {e}")
            return super().form_invalid(form)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ... additional context data setup ...
        return context

class JobPageViewSet(viewsets.ModelViewSet):
    serializer_class = JobPageSerializer

    def get_queryset(self):
        """
        Optionally filter the pages to those that are public based on a condition.
        For example, the condition can be based on a query parameter or a setting.
        """
        queryset = JobPage.objects.live()

        # Here we check a condition - for example, checking a query parameter
        if 'public' in self.request.query_params:
            # Only return public pages if 'public' query parameter is provided
            return queryset.public().order_by('-first_published_at')
        else:
            return queryset.all()