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
class Industry(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class ContactIntern(models.Model):
    job_page = ParentalKey('JobPage', related_name='contact_interns', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('linkedin'),
        FieldPanel('email'),
    ]
class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.name}"

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
class Industry(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

class JobPage(Page, ClusterableModel):
    parent_page_types = ['JobIndexPage']
    subpage_types = []

    JOB_TYPE_CHOICES = [
        ('remote', 'Remote'),
        ('full time', 'Full Time'),
        ('part time', 'Part Time'),
    ]

    MONTH_CHOICES = [
        ('01', 'January'),
        ('02', 'February'),
        ('03', 'March'),
        ('04', 'April'),
        ('05', 'May'),
        ('06', 'June'),
        ('07', 'July'),
        ('08', 'August'),
        ('09', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
    ]

    industry = models.ForeignKey(Industry, on_delete=models.SET_NULL, null=True, blank=True)
    categories = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    job_title = models.CharField(max_length=255, blank=True)
    company_name = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    contract_type = models.CharField(max_length=255, choices=JOB_TYPE_CHOICES, blank=True)
    duration = models.IntegerField(blank=True, null=True, help_text="Duration in months")
    month = models.CharField(max_length=2, choices=MONTH_CHOICES, blank=True, null=True)
    job_description = RichTextField(blank=True)
    notes_feedbacks = RichTextField(blank=True)
    language_requirements = models.CharField(max_length=255, blank=True)
    expected_salary = models.CharField(max_length=255, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True, related_name='jobs')
    new_currency_code = models.CharField(max_length=3, blank=True, help_text="Currency code (e.g., USD)")
    coding_languages = models.CharField(max_length=255, blank=True)
    asset_class = models.CharField(max_length=255, blank=True)
    interview_report_link = models.URLField(blank=True)
    new_company_name = models.CharField(max_length=255, blank=True, help_text="Add a new company if it's not listed")
    new_city_name = models.CharField(max_length=255, blank=True, help_text="Add a new city if it's not listed")
    new_industry_name = models.CharField(max_length=255, blank=True, help_text="Add a new industry if it's not listed")
    new_category_name = models.CharField(max_length=255, blank=True, help_text="Add a new category if it's not listed")

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('industry'),
            FieldPanel('new_industry_name'),
            FieldPanel('categories'),
            FieldPanel('new_category_name'),
            FieldPanel('job_title'),
            FieldPanel('company_name'),
            FieldPanel('new_company_name'),
            FieldPanel('location'),
            FieldPanel('new_city_name'),
            FieldPanel('contract_type'),
            FieldPanel('duration'),
            FieldPanel('month'),
            FieldPanel('job_description'),
            FieldPanel('notes_feedbacks'),
            FieldPanel('language_requirements'),
            FieldPanel('expected_salary'),
            FieldPanel('currency'),
            FieldPanel('new_currency_code'),

            FieldPanel('coding_languages'),
            FieldPanel('asset_class'),
            FieldPanel('interview_report_link'),
        ], heading="Job Details"),
        MultiFieldPanel([
            InlinePanel('contact_persons', label="Contact Persons"),
        ], heading="Contact Persons"),
        MultiFieldPanel([
            InlinePanel('contact_interns', label="Contact interns"),
        ], heading="Contact interns"),
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

        if self.new_industry_name:
            new_industry, created = Industry.objects.get_or_create(name=self.new_industry_name)
            self.industry = new_industry
            self.new_industry_name = ''  # Clear the field after saving

        if self.new_category_name:
            new_category, created = Category.objects.get_or_create(name=self.new_category_name)
            self.categories = new_category
            self.new_category_name = ''  # Clear the field after saving

        if self.new_currency_code:
            new_currency, created = Currency.objects.get_or_create(code=self.new_currency_code)
            self.currency = new_currency
            self.new_currency_code = ''

        super().save(*args, **kwargs)
