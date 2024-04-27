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
from .views import JobPageViewSet, JobImportView, ExcelUploadView

router = DefaultRouter()
router.register(r'jobs', JobPageViewSet, basename='jobpage')

urlpatterns = [
    path('', include(router.urls)),
    path('import-jobs/', JobImportView.as_view(), name='job_import'),
    path('upload_excel/', ExcelUploadView.as_view(), name='upload_excel'),
]
