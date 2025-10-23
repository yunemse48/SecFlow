"""
URL configuration for change requests app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ChangeRequestViewSet,
    ChangeRequestCommentViewSet,
    ChangeRequestAttachmentViewSet
)

router = DefaultRouter()
router.register(r'', ChangeRequestViewSet, basename='changerequest')
router.register(r'comments', ChangeRequestCommentViewSet, basename='changerequest-comment')
router.register(r'attachments', ChangeRequestAttachmentViewSet, basename='changerequest-attachment')

urlpatterns = [
    path('', include(router.urls)),
]
