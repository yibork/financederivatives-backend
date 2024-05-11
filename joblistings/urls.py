
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import job_search
from django.conf import settings
from .views import JobPageViewSet, JobImportView, ExcelUploadView
router = DefaultRouter()
router.register(r'jobs', JobPageViewSet, basename='jobpage')
urlpatterns = [
    path('', include(router.urls)),
    path('import-jobs/', JobImportView.as_view(), name='job_import'),
    path('upload_excel/', ExcelUploadView.as_view(), name='upload_excel'),
        path('job_search/', job_search, name='job_search'),


]

# Conditionally add debug toolbar routes in development mode
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns