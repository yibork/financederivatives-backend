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
    search_term = request.GET.get('search_term', 'Engineer')  # Default to 'Engineer' if not specified
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
