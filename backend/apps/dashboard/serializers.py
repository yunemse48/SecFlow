"""
Serializers for dashboard app.
"""

from rest_framework import serializers


class DashboardStatsSerializer(serializers.Serializer):
    """
    Serializer for dashboard statistics.
    """
    total_change_requests = serializers.IntegerField()
    pending_change_requests = serializers.IntegerField()
    in_progress_change_requests = serializers.IntegerField()
    completed_change_requests = serializers.IntegerField()
    
    total_analyses = serializers.IntegerField()
    active_analyses = serializers.IntegerField()
    completed_analyses = serializers.IntegerField()
    
    total_findings = serializers.IntegerField()
    critical_findings = serializers.IntegerField()
    high_findings = serializers.IntegerField()
    open_findings = serializers.IntegerField()
    
    avg_analysis_time_hours = serializers.FloatField()
