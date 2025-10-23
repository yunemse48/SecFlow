"""
Views for change requests app.
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import ChangeRequest, ChangeRequestComment, ChangeRequestAttachment
from .serializers import (
    ChangeRequestSerializer,
    ChangeRequestDetailSerializer,
    ChangeRequestCommentSerializer,
    ChangeRequestAttachmentSerializer
)


class ChangeRequestViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing change requests.
    """
    queryset = ChangeRequest.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'source', 'assigned_to']
    search_fields = ['external_id', 'title', 'description', 'requester']
    ordering_fields = ['created_at', 'updated_at', 'requested_date', 'priority']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ChangeRequestDetailSerializer
        return ChangeRequestSerializer
    
    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        """
        Assign a change request to a user.
        """
        change_request = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'user_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        try:
            user = User.objects.get(id=user_id)
            change_request.assigned_to = user
            change_request.save()
            
            serializer = self.get_serializer(change_request)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """
        Update the status of a change request.
        """
        change_request = self.get_object()
        new_status = request.data.get('status')
        
        if not new_status:
            return Response(
                {'error': 'status is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if new_status not in dict(ChangeRequest.Status.choices):
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        change_request.status = new_status
        
        if new_status == ChangeRequest.Status.COMPLETED:
            from django.utils import timezone
            change_request.completed_date = timezone.now()
        
        change_request.save()
        
        serializer = self.get_serializer(change_request)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_requests(self, request):
        """
        Get change requests assigned to the current user.
        """
        queryset = self.filter_queryset(
            self.get_queryset().filter(assigned_to=request.user)
        )
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ChangeRequestCommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing change request comments.
    """
    queryset = ChangeRequestComment.objects.all()
    serializer_class = ChangeRequestCommentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        change_request_id = self.request.query_params.get('change_request')
        
        if change_request_id:
            queryset = queryset.filter(change_request_id=change_request_id)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ChangeRequestAttachmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing change request attachments.
    """
    queryset = ChangeRequestAttachment.objects.all()
    serializer_class = ChangeRequestAttachmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        change_request_id = self.request.query_params.get('change_request')
        
        if change_request_id:
            queryset = queryset.filter(change_request_id=change_request_id)
        
        return queryset
    
    def perform_create(self, serializer):
        file = self.request.FILES.get('file')
        serializer.save(
            uploaded_by=self.request.user,
            filename=file.name,
            file_size=file.size
        )
