from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
class JobIndexPage(Page):
    subpage_types = ['joblistings.JobPage']  # This allows only JobPage children
    max_count = 1  # Optional: use if you want only one Job Index Page

    content_panels = Page.content_panels + [
        # Add panels for any fields you define on your index page
    ]
    template = "joblistings/job_index_page.html"


class JobPage(Page):
    parent_page_types = ['joblistings.JobIndexPage']
    subpage_types = []  # No child pages
    job_title = models.CharField(max_length=255, blank=True)
    company_name = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    profile = RichTextField(blank=True)
    job_type = models.CharField(max_length=255, blank=True)
    industry = models.CharField(max_length=255, blank=True)
    department = models.CharField(max_length=255, blank=True)
    experience_level = models.CharField(max_length=255, blank=True)
    education_level = models.CharField(max_length=255, blank=True)
    skills_required = RichTextField(blank=True)
    responsibilities = RichTextField(blank=True)
    job_company_description = RichTextField(blank=True)
    language_requirements = models.CharField(max_length=255, blank=True)
    salary_range = models.CharField(max_length=255, blank=True)
    benefits = RichTextField(blank=True)
    work_hours = models.CharField(max_length=255, blank=True)
    remote_work = models.BooleanField(default=False, blank=True)
    travel_requirements = models.CharField(max_length=255, blank=True)
    full_description = RichTextField(blank=True)
    contact_information = RichTextField(blank=True)
    application_link_email = models.URLField(blank=True)
    how_to_apply = RichTextField(blank=True)
    post_date = models.DateField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    ex_current_intern_link = models.URLField(blank=True)
    ex_current_linkedin_link = models.URLField(blank=True)
    professional_1_name = models.CharField(max_length=255, blank=True)
    contact_person_1_linkedin = models.URLField(blank=True)
    mail_professional_1 = models.EmailField(blank=True)
    contact_person_2_name = models.CharField(max_length=255, blank=True)
    contact_person_2_linkedin = models.URLField(blank=True)
    contact_person_3_name = models.CharField(max_length=255, blank=True)
    contact_person_3_linkedin = models.URLField(blank=True)
    link_linkedin_offer = models.URLField(blank=True)
    template = "joblistings/job_page.html"

    content_panels = Page.content_panels + [
        FieldPanel('job_title'),
        FieldPanel('company_name'),
        FieldPanel('location'),
        FieldPanel('profile'),
        FieldPanel('job_type'),
        FieldPanel('industry'),
        FieldPanel('department'),
        FieldPanel('experience_level'),
        FieldPanel('education_level'),
        FieldPanel('skills_required'),
        FieldPanel('responsibilities'),
        FieldPanel('job_company_description'),
        FieldPanel('language_requirements'),
        FieldPanel('salary_range'),
        FieldPanel('benefits'),
        FieldPanel('work_hours'),
        FieldPanel('remote_work'),
        FieldPanel('travel_requirements'),
        FieldPanel('full_description'),
        FieldPanel('contact_information'),
        FieldPanel('application_link_email'),
        FieldPanel('how_to_apply'),
        FieldPanel('post_date'),
        FieldPanel('start_date'),
        FieldPanel('ex_current_intern_link'),
        FieldPanel('ex_current_linkedin_link'),
        FieldPanel('professional_1_name'),
        FieldPanel('contact_person_1_linkedin'),
        FieldPanel('mail_professional_1'),
        FieldPanel('contact_person_2_name'),
        FieldPanel('contact_person_2_linkedin'),
        FieldPanel('contact_person_3_name'),
        FieldPanel('contact_person_3_linkedin'),
        FieldPanel('link_linkedin_offer'),
    ]

