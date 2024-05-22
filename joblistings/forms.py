# forms.py in your wagtail app
from django import forms
from .models import City, Company, JobPage

class JobImportForm(forms.Form):
    excel_file = forms.FileField()

class JobPageForm(forms.ModelForm):
    new_city = forms.CharField(required=False, help_text="Enter a new city if it doesn't exist in the list.")
    new_company = forms.CharField(required=False, help_text="Enter a new company if it doesn't exist in the list.")

    class Meta:
        model = JobPage
        fields = '__all__'

    def save(self, commit=True):
        new_city = self.cleaned_data.get('new_city')
        new_company = self.cleaned_data.get('new_company')

        if new_city:
            city, created = City.objects.get_or_create(name=new_city)
            self.instance.location = city

        if new_company:
            company, created = Company.objects.get_or_create(name=new_company)
            self.instance.company_name = company

        return super().save(commit=commit)
