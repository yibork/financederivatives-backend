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
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import requests

# Configure your Google Cloud credentials
dir_path = os.path.dirname(os.path.realpath(__file__))
SERVICE_ACCOUNT_FILE =  os.path.join(dir_path, 'secret', 'dashboard-finance-derivatives-0b16f2f20dc3.json')
SCOPES = ['https://www.googleapis.com/auth/jobs']
print("Attempting to load credentials from:", SERVICE_ACCOUNT_FILE)
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

client_service = build('jobs', 'v3', credentials=credentials)
project_id = 'projects/dashboard-finance-derivatives'

#fetch data from indeed
def fetch_indeed_jobs():
    url = "https://indeed11.p.rapidapi.com/"
    payload = {
        "search_terms": "Engineer",
        "location": "United States",
        "page": "1"
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "3cbf12bb91msh67c4b738331dd30p1908c8jsn89e563d7fccb",
        "X-RapidAPI-Host": "indeed11.p.rapidapi.com"
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


def transform_to_google_format(indeed_jobs):
    google_jobs = []
    uniqId = uuid.UUID
    for job in indeed_jobs:
        google_job = {
            "job": {
                "title": job['job_title'],
                "companyName": job['company_name'],
                "description": job['summary'],
                "addresses": [job['location']],
                "requisitionId": uniqId,  # This should be unique
                "applicationInfo": {
                    "uris": [job['url']]
                },
                "postingPublishTime": "2024-05-10T12:00:00Z",  # Example timestamp
                "postingExpireTime": "2024-06-10T12:00:00Z"
            }
        }
        google_jobs.append(google_job)

    return google_jobs
        
        
def post_indeed_jobs_to_google(request):
    # Fetch jobs from Indeed (assuming `fetch_indeed_jobs()` is already implemented)
    indeed_jobs = fetch_indeed_jobs()
    print('Indeed jobs: ', indeed_jobs)
    return JsonResponse({'Jobs': indeed_jobs})
    # rest of the code for case of storing data in
    google_jobs = transform_to_google_format(indeed_jobs)
    body = {"jobs": google_jobs}
    print('Google jobs: ', google_jobs)
    return JsonResponse({'Jobs': google_jobs})
    # Post jobs to Google Cloud Talent Solution
    #response = client_service.projects().tenants().jobs().batchCreate(
    #    parent='projects/dashboard-finance-derivatives/tenants/fahd-g7o51', 
    #    body=body
    #).execute()
    #print('Response: ', response)


        
@csrf_exempt
@require_http_methods(["POST"])  # Ensuring only POST requests are handled
def job_search(request):
    if request.method != 'POST':
        return JsonResponse({'message': 'Invalid request method, POST required'}, status=405)
    # Hardcoding the job type in the query
    search_term = 'Engineer'  # Default to 'Engineer' if not specified
    job_categories = ['SCIENCE_AND_ENGINEERING']  # Example category, adjust as necessary

    request_metadata = {
    'domain': 'yourcompanydomain.com',
    'session_id': str(request.session.session_key),  # Assuming session is being used
    'user_id': str(request.user.id) if request.user.is_authenticated else 'anonymous'
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
    print('Request body: ', body)
    response = client_service.projects().jobs().search(parent=project_id, body=body).execute()
    if 'error' in response:
        print('Error response: ', response['error'])
        return JsonResponse({'message': 'Error processing your request', 'details': response['error']}, status=500)

    print('API response: ', response)
    jobs = response.get('matchingJobs', [])
    print(jobs)
    if not jobs:
        return JsonResponse({'message': 'No Job Results'}, status=404)

    results = [{
        'title': job.get('job', {}).get('title'),
        'description': job.get('job', {}).get('description')
    } for job in jobs]

    return JsonResponse({'jobs': results})
