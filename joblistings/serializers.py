# serializers.py
from rest_framework import serializers
from .models import JobPage


from .models import JobPage, Company, City, Industry, Category, Currency
class JobPageSerializer(serializers.ModelSerializer):
    company_name = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    contact_persons = serializers.SerializerMethodField()
    contact_interns = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    industry = serializers.SerializerMethodField()
    coding_languages = serializers.SerializerMethodField()
    coding_languages_ids = serializers.SerializerMethodField()
    month = serializers.SerializerMethodField()
    location_ids = serializers.SerializerMethodField()
    category_ids = serializers.SerializerMethodField()
    industry_ids = serializers.SerializerMethodField()
    company_name_ids = serializers.SerializerMethodField()
    currency = serializers.SerializerMethodField()
    currency_ids = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    language_requirements = serializers.SerializerMethodField()
    language_requirements_ids = serializers.SerializerMethodField()
    class Meta:
        model = JobPage
        fields = '__all__'
    def get_language_requirements(self, obj):
        return [language.name for language in obj.language_requirements.all()]

    def get_language_requirements_ids(self, obj):
        return [language.id for language in obj.language_requirements.all()]

    def get_category_ids(self, obj):
        return obj.categories.id if obj.categories else None
    
    def get_industry_ids(self, obj):
        return obj.industry.id if obj.industry else None
    
    def get_company_name_ids(self, obj):
        return obj.company_name.id if obj.company_name else None
    
    def get_currency_ids(self, obj):
        return obj.currency.id if obj.currency else None
    
    def get_currency(self, obj):
        return obj.currency.code if obj.currency else None
    
    def get_category(self, obj):
        return obj.categories.name if obj.categories else None

    def get_month(self, obj):
        month_mapping = {
            '01': 'January', '02': 'February', '03': 'March', '04': 'April',
            '05': 'May', '06': 'June', '07': 'July', '08': 'August',
            '09': 'September', '10': 'October', '11': 'November', '12': 'December'
        }
        return month_mapping.get(obj.month, 'Unknown')

    def get_coding_languages(self, obj):
        return [language.name for language in obj.coding_languages.all()] if obj.coding_languages else []
    def get_coding_languages_ids(self, obj):
        return [language.id for language in obj.coding_languages.all()] if obj.coding_languages else []
    def get_industry(self, obj):
        return obj.industry.name if obj.industry else None

    def get_company_name(self, obj):
        return obj.company_name.name if obj.company_name else None

    def get_location_ids(self, obj):
        if obj.location:
            return obj.location.id
        return None
    def get_location(self, obj):
        if obj.location:
            return obj.location.name
        return None
    def get_contact_persons(self, obj):
        return obj.contact_persons.all().values()

    def get_contact_interns(self, obj):
        return obj.contact_interns.all().values()

class JobPageAddSerializer(serializers.ModelSerializer):
    new_company_name = serializers.CharField(required=False, allow_blank=True)
    new_city_name = serializers.CharField(required=False, allow_blank=True)
    new_industry_name = serializers.CharField(required=False, allow_blank=True)
    new_category_name = serializers.CharField(required=False, allow_blank=True)
    contact_persons = serializers.ListField(child=serializers.DictField(), required=False)
    contact_interns = serializers.ListField(child=serializers.DictField(), required=False)
    coding_languages = serializers.ListField(child=serializers.CharField(), required=False)
    language_requirements = serializers.ListField(child=serializers.CharField(), required=False)
    company_name = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), required=False, allow_null=True)
    location = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), required=False, allow_null=True)
    industry = serializers.PrimaryKeyRelatedField(queryset=Industry.objects.all(), required=False, allow_null=True)
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False, allow_null=True)
    currency = serializers.PrimaryKeyRelatedField(queryset=Currency.objects.all(), required=False, allow_null=True)
    class Meta:
        model = JobPage
        fields = [
            'job_title', 'company_name', 'new_company_name', 'location', 'new_city_name',
            'industry', 'new_industry_name', 'categories', 'new_category_name', 'contract_type',
            'duration', 'month', 'job_description', 'notes_feedbacks', 'language_requirements',
            'expected_salary', 'currency', 'new_currency_code', 'coding_languages', 'asset_class',
            'interview_report_link', 'contact_persons', 'contact_interns'
        ]
