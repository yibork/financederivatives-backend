# serializers.py
from rest_framework import serializers
from .models import JobPage

class JobPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPage
        fields = '__all__'

class JobPageAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPage
        fields = ['job_title', 'company_name', 'location', 'job_type']
