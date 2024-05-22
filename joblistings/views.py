from django.forms import ValidationError
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView
from wagtail.admin.messages import success, error
from .forms import JobImportForm
from .models import JobPage, JobIndexPage, Company, City
from openpyxl import load_workbook
from rest_framework.generics import ListAPIView
from .serializers import JobPageSerializer, JobPageAddSerializer
import os
from django.http import JsonResponse
from django.views import View
from django.core.management import call_command
from django.core.files.storage import default_storage
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from wagtail.models import Page
from dal import autocomplete
import uuid
from googleapiclient.discovery import build
from google.oauth2 import service_account

class CompanyAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Company.objects.none()

        qs = Company.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs

class CityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return City.objects.none()

        qs = City.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs

# Fetch data from Indeed
def fetch_indeed_jobs(request):
    file_path = 'indeed_jobs.json'
    url = "https://indeed11.p.rapidapi.com/"
    payload = {"search_terms": "Engineer", "location": "United States", "page": "1"}
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "3cbf12bb91msh67c4b738331dd30p1908c8jsn89e563d7fccb",
        "X-RapidAPI-Host": "indeed11.p.rapidapi.com"
    }
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    return JsonResponse(data)

@method_decorator(csrf_exempt, name='dispatch')
class JobPageAddViewSet(viewsets.ModelViewSet):
    queryset = JobPage.objects.all()
    serializer_class = JobPageAddSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        job_title = request.data.get('job_title')
        company_name = request.data.get('company_name')
        location = request.data.get('location')
        job_type = request.data.get('job_type')
        contact_person_name = request.data.get('contact_person')
        contact_person_linkedin = request.data.get('contact_person_linkedin')

        if not job_title or not company_name or not location or not job_type:
            return Response(
                {"error": "job_title, company_name, location, and job_type are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        job_index, created = JobIndexPage.objects.get_or_create(
            title="Job Index Page",
            defaults={'title': 'Job Index Page', 'slug': 'job-index-page', 'depth': 1, 'path': '000100012'}
        )

        if created:
            root = Page.get_first_root_node()
            job_index = root.add_child(instance=job_index)
        else:
            job_index = JobIndexPage.objects.get(title="Job Index Page")

        slug = slugify(job_title) + '-' + str(uuid.uuid4())[:8]

        job_page = JobPage(
            title=job_title,
            slug=slug,
            job_title=job_title,
            company_name=company_name,
            location=location,
            job_type=job_type,
            contact_person_1_name=contact_person_name,
            contact_person_1_linkedin=contact_person_linkedin,
            owner=user,
            live=False,
        )

        try:
            job_page.full_clean()
            job_index.add_child(instance=job_page)
            job_page.unpublish()
            return Response({"message": "Job added successfully."}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)

def transform_to_google_format(indeed_jobs):
    google_jobs = []
    for job in indeed_jobs:
        google_job = {
            "job": {
                "title": job['job_title'],
                "companyName": job['company_name'],
                "description": job['summary'],
                "addresses": [job['location']],
                "requisitionId": str(uuid.uuid4()),  # Generate unique ID
                "applicationInfo": {"uris": [job['url']]},
                "postingPublishTime": "2024-05-10T12:00:00Z",
                "postingExpireTime": "2024-06-10T12:00:00Z"
            }
        }
        google_jobs.append(google_job)
    return google_jobs

def post_indeed_jobs_to_google(request):
    file_path = 'indeed_jobs.json'
    try:
        with open(file_path, 'r') as file:
            indeed_jobs = json.load(file)
    except FileNotFoundError:
        return JsonResponse({'error': 'Job data file not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Error decoding JSON data'}, status=500)

    google_jobs = transform_to_google_format(indeed_jobs)
    body = {"jobs": google_jobs}
    return JsonResponse({'Jobs': google_jobs})

class ExcelUploadView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'admin/excel_upload_form.html')

    def post(self, request, *args, **kwargs):
        excel_file = request.FILES.get('excel_file')
        if not excel_file:
            return JsonResponse({'error': 'No file uploaded.'}, status=400)

        file_path = default_storage.save('tmp/excel_file.xlsx', excel_file)
        full_file_path = default_storage.path(file_path)

        try:
            call_command('import_jobs', full_file_path)
            return JsonResponse({'success': 'Jobs imported successfully.'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        finally:
            os.remove(full_file_path)

class JobImportView(FormView):
    template_name = 'job_import.html'
    form_class = JobImportForm
    success_url = reverse_lazy('wagtailadmin_home')

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
        return context

class JobPageViewSet(viewsets.ModelViewSet):
    serializer_class = JobPageSerializer

    def get_queryset(self):
        queryset = JobPage.objects.live()
        if 'public' in self.request.query_params:
            return queryset.public().order_by('-first_published_at')
        return queryset.all()
