"""
URL configuration for security analysis app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    SecurityAnalysisViewSet,
    ScanTypeViewSet,
    ScanViewSet,
    FindingViewSet
)

router = DefaultRouter()
router.register(r'', SecurityAnalysisViewSet, basename='security-analysis')
router.register(r'scan-types', ScanTypeViewSet, basename='scan-type')
router.register(r'scans', ScanViewSet, basename='scan')
router.register(r'findings', FindingViewSet, basename='finding')

urlpatterns = [
    path('', include(router.urls)),
]
