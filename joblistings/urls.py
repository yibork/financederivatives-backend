# # urls.py
# from django.urls import path
# from .views import JobPageList, JobImportView, ExcelUploadView

# urlpatterns = [
#     path('jobs/', JobPageList.as_view(), name='api_jobs'),
#     path('import-jobs/', JobImportView.as_view(), name='job_import'),
#     path('upload_excel/', ExcelUploadView.as_view(), name='upload_excel'),


# ]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import post_indeed_jobs_to_google, fetch_indeed_jobs #, job_search
from .views import JobPageViewSet, JobImportView, ExcelUploadView, JobPageAddViewSet
from .views import CompanyAutocomplete, CityAutocomplete

from django.conf import settings
router = DefaultRouter()
router.register(r'jobs', JobPageViewSet, basename='jobpage')
router.register(r'add_jobs', JobPageAddViewSet, basename='jobpageadd')

urlpatterns = [
        path('', include(router.urls)),
#    path('job_search/', job_search, name='job_search'),
    path('job_list/', post_indeed_jobs_to_google, name='job_list'),
    path('job_fetch/', fetch_indeed_jobs, name='job_fetch'),
        path('company-autocomplete/', CompanyAutocomplete.as_view(), name='company-autocomplete'),
    path('city-autocomplete/', CityAutocomplete.as_view(), name='city-autocomplete'),

]

# Conditionally add debug toolbar routes in development mode
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns