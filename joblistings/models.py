from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.fields import RichTextField
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

class City(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class JobIndexPage(Page):
    subpage_types = ['JobPage']
    max_count = 1

    content_panels = Page.content_panels + [
        # Add panels for any fields you define on your index page
    ]
    template = "joblistings/job_index_page.html"

class ContactPerson(models.Model):
    job_page = ParentalKey('JobPage', related_name='contact_persons', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('linkedin'),
        FieldPanel('email'),
    ]

class JobPage(Page, ClusterableModel):
    parent_page_types = ['JobIndexPage']
    subpage_types = []
    JOB_TYPE_CHOICES = [
        ('remote', 'Remote'),
        ('full time', 'Full Time'),
        ('part time', 'Part Time'),
    ]

    industry = models.CharField(max_length=255, blank=True)
    categories = models.CharField(max_length=255, blank=True)
    job_title = models.CharField(max_length=255, blank=True)
    company_name = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    contract_type = models.CharField(max_length=255, choices=JOB_TYPE_CHOICES, blank=True)
    duration = models.IntegerField(blank=True, null=True, help_text="Duration in months")
    start_date = models.DateField(blank=True, null=True)
    job_description = RichTextField(blank=True)
    notes_feedbacks = RichTextField(blank=True)
    language_requirements = models.CharField(max_length=255, blank=True)
    expected_salary = models.CharField(max_length=255, blank=True)
    coding_languages = models.CharField(max_length=255, blank=True)
    asset_class = models.CharField(max_length=255, blank=True)
    interview_report_link = models.URLField(blank=True)
    new_company_name = models.CharField(max_length=255, blank=True, help_text="Add a new company if it's not listed")
    new_city_name = models.CharField(max_length=255, blank=True, help_text="Add a new city if it's not listed")

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('industry'),
            FieldPanel('categories'),
            FieldPanel('job_title'),
            FieldPanel('company_name'),
            FieldPanel('new_company_name'),
            FieldPanel('location'),
            FieldPanel('new_city_name'),
            FieldPanel('contract_type'),
            FieldPanel('duration'),
            FieldPanel('start_date'),
            FieldPanel('job_description'),
            FieldPanel('notes_feedbacks'),
            FieldPanel('language_requirements'),
            FieldPanel('expected_salary'),
            FieldPanel('coding_languages'),
            FieldPanel('asset_class'),
            FieldPanel('interview_report_link'),
        ], heading="Job Details"),
        MultiFieldPanel([
            InlinePanel('contact_persons', label="Contact Persons"),
        ], heading="Contact Persons"),
    ]

    template = "joblistings/job_page.html"

    def save(self, *args, **kwargs):
        if self.new_company_name:
            new_company, created = Company.objects.get_or_create(name=self.new_company_name)
            self.company_name = new_company
            self.new_company_name = ''  # Clear the field after saving
        
        if self.new_city_name:
            new_city, created = City.objects.get_or_create(name=self.new_city_name)
            self.location = new_city
            self.new_city_name = ''  # Clear the field after saving

        super().save(*args, **kwargs)
