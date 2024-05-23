# serializers.py
from rest_framework import serializers
from .models import JobPage

class JobPageSerializer(serializers.ModelSerializer):
    company_name = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    contact_persons = serializers.SerializerMethodField()

    class Meta:
        model = JobPage
        fields = '__all__'

    def get_company_name(self, obj):
        return obj.company_name.name if obj.company_name else None
    def get_location(self, obj):
        return obj.location.name if obj.location else None
    def get_contact_persons(self, obj):
        return obj.contact_persons.all().values()

class JobPageAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPage
        fields = ['industry','categories', 'job_title', 'company_name', 'new_company_name', 'location', 'new_city_name', 'contract_type', 'duration', 'start_month', 'job_description', 'notes_feedbacks', 'language_requirements', 'expected_salary', 'coding_languages', 'asset_class', 'interview_report_link']