"""
Views for dashboard app.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q, Avg, F
from datetime import timedelta

from apps.change_requests.models import ChangeRequest
from apps.security_analysis.models import SecurityAnalysis, Finding
from .serializers import DashboardStatsSerializer


class DashboardStatsView(APIView):
    """
    View for retrieving dashboard statistics.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Get overall dashboard statistics.
        """
        # Change Request stats
        total_change_requests = ChangeRequest.objects.count()
        pending_change_requests = ChangeRequest.objects.filter(
            status=ChangeRequest.Status.PENDING
        ).count()
        in_progress_change_requests = ChangeRequest.objects.filter(
            status=ChangeRequest.Status.IN_PROGRESS
        ).count()
        completed_change_requests = ChangeRequest.objects.filter(
            status=ChangeRequest.Status.COMPLETED
        ).count()
        
        # Security Analysis stats
        total_analyses = SecurityAnalysis.objects.count()
        active_analyses = SecurityAnalysis.objects.filter(
            status=SecurityAnalysis.Status.IN_PROGRESS
        ).count()
        completed_analyses = SecurityAnalysis.objects.filter(
            status=SecurityAnalysis.Status.COMPLETED
        ).count()
        
        # Finding stats
        total_findings = Finding.objects.count()
        critical_findings = Finding.objects.filter(
            severity=Finding.Severity.CRITICAL,
            status=Finding.Status.OPEN
        ).count()
        high_findings = Finding.objects.filter(
            severity=Finding.Severity.HIGH,
            status=Finding.Status.OPEN
        ).count()
        open_findings = Finding.objects.filter(
            status=Finding.Status.OPEN
        ).count()
        
        # Calculate average analysis time
        completed_analyses_with_time = SecurityAnalysis.objects.filter(
            status=SecurityAnalysis.Status.COMPLETED,
            started_at__isnull=False,
            completed_at__isnull=False
        )
        
        avg_analysis_time_hours = 0
        if completed_analyses_with_time.exists():
            total_seconds = sum([
                (analysis.completed_at - analysis.started_at).total_seconds()
                for analysis in completed_analyses_with_time
            ])
            avg_analysis_time_hours = round(
                total_seconds / completed_analyses_with_time.count() / 3600, 2
            )
        
        data = {
            'total_change_requests': total_change_requests,
            'pending_change_requests': pending_change_requests,
            'in_progress_change_requests': in_progress_change_requests,
            'completed_change_requests': completed_change_requests,
            'total_analyses': total_analyses,
            'active_analyses': active_analyses,
            'completed_analyses': completed_analyses,
            'total_findings': total_findings,
            'critical_findings': critical_findings,
            'high_findings': high_findings,
            'open_findings': open_findings,
            'avg_analysis_time_hours': avg_analysis_time_hours,
        }
        
        serializer = DashboardStatsSerializer(data)
        return Response(serializer.data)


class MyDashboardView(APIView):
    """
    View for retrieving user-specific dashboard data.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Get dashboard data for the current user.
        """
        user = request.user
        
        # User's assigned change requests
        my_change_requests = ChangeRequest.objects.filter(
            assigned_to=user
        ).values('status').annotate(count=Count('id'))
        
        # User's security analyses
        my_analyses = SecurityAnalysis.objects.filter(
            analyst=user
        ).values('status').annotate(count=Count('id'))
        
        # Recent activity
        recent_change_requests = ChangeRequest.objects.filter(
            assigned_to=user
        ).order_by('-updated_at')[:5].values(
            'id', 'external_id', 'title', 'status', 'priority', 'updated_at'
        )
        
        return Response({
            'my_change_requests': list(my_change_requests),
            'my_analyses': list(my_analyses),
            'recent_change_requests': list(recent_change_requests),
        })
