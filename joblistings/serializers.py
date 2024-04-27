# serializers.py
from rest_framework import serializers
from .models import JobPage

class JobPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPage
        fields = [
            'id', 'title', 'job_title', 'company_name', 'location',
            'profile', 'job_type', 'industry', 'department', 'experience_level',
            'education_level', 'skills_required', 'responsibilities',
            'job_company_description', 'language_requirements', 'salary_range',
            'benefits', 'work_hours', 'remote_work', 'travel_requirements',
            'full_description', 'contact_information', 'application_link_email',
            'how_to_apply', 'post_date', 'start_date'
        ]
