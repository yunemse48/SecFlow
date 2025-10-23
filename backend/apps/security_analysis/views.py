"""
Views for security analysis app.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from .models import SecurityAnalysis, ScanType, Scan, Finding
from .serializers import (
    SecurityAnalysisSerializer,
    SecurityAnalysisDetailSerializer,
    ScanTypeSerializer,
    ScanSerializer,
    ScanDetailSerializer,
    FindingSerializer
)


class SecurityAnalysisViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing security analyses.
    """
    queryset = SecurityAnalysis.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'analyst', 'change_request']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SecurityAnalysisDetailSerializer
        return SecurityAnalysisSerializer
    
    def perform_create(self, serializer):
        serializer.save(analyst=self.request.user)
    
    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """
        Start a security analysis.
        """
        analysis = self.get_object()
        
        if analysis.status != SecurityAnalysis.Status.NOT_STARTED:
            return Response(
                {'error': 'Analysis already started'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        analysis.status = SecurityAnalysis.Status.IN_PROGRESS
        analysis.started_at = timezone.now()
        analysis.save()
        
        serializer = self.get_serializer(analysis)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """
        Complete a security analysis.
        """
        analysis = self.get_object()
        
        if analysis.status != SecurityAnalysis.Status.IN_PROGRESS:
            return Response(
                {'error': 'Analysis is not in progress'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        analysis.status = SecurityAnalysis.Status.COMPLETED
        analysis.completed_at = timezone.now()
        analysis.risk_score = request.data.get('risk_score', analysis.risk_score)
        analysis.notes = request.data.get('notes', analysis.notes)
        analysis.save()
        
        serializer = self.get_serializer(analysis)
        return Response(serializer.data)


class ScanTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing scan types.
    """
    queryset = ScanType.objects.all()
    serializer_class = ScanTypeSerializer
    permission_classes = [IsAuthenticated]


class ScanViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing scans.
    """
    queryset = Scan.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'scan_type', 'security_analysis']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ScanDetailSerializer
        return ScanSerializer
    
    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """
        Start a scan execution.
        """
        scan = self.get_object()
        
        if scan.status != Scan.Status.QUEUED:
            return Response(
                {'error': 'Scan already started'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        scan.status = Scan.Status.RUNNING
        scan.started_at = timezone.now()
        scan.save()
        
        # TODO: Trigger actual scan execution via Celery task
        
        serializer = self.get_serializer(scan)
        return Response(serializer.data)


class FindingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing findings.
    """
    queryset = Finding.objects.all()
    serializer_class = FindingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['severity', 'status', 'scan']
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """
        Update the status of a finding.
        """
        finding = self.get_object()
        new_status = request.data.get('status')
        
        if not new_status or new_status not in dict(Finding.Status.choices):
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        finding.status = new_status
        finding.save()
        
        serializer = self.get_serializer(finding)
        return Response(serializer.data)
