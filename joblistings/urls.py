# urls.py
from django.urls import path
from .views import JobPageList, JobImportView, ExcelUploadView

urlpatterns = [
    path('jobs/', JobPageList.as_view(), name='api_jobs'),
    path('import-jobs/', JobImportView.as_view(), name='job_import'),
    path('upload_excel/', ExcelUploadView.as_view(), name='upload_excel'),


]
