"""
Serializers for security analysis app.
"""

from rest_framework import serializers
from .models import SecurityAnalysis, ScanType, Scan, Finding


class ScanTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for ScanType model.
    """
    
    class Meta:
        model = ScanType
        fields = [
            'id', 'name', 'description', 'is_active',
            'configuration', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class FindingSerializer(serializers.ModelSerializer):
    """
    Serializer for Finding model.
    """
    
    class Meta:
        model = Finding
        fields = [
            'id', 'scan', 'title', 'description', 'severity', 'status',
            'cwe_id', 'file_path', 'line_number', 'remediation',
            'external_ticket_id', 'metadata', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ScanSerializer(serializers.ModelSerializer):
    """
    Serializer for Scan model.
    """
    scan_type_name = serializers.CharField(source='scan_type.name', read_only=True)
    findings_summary = serializers.SerializerMethodField()
    
    class Meta:
        model = Scan
        fields = [
            'id', 'security_analysis', 'scan_type', 'scan_type_name', 'status',
            'started_at', 'completed_at', 'duration_seconds', 'findings_count',
            'critical_count', 'high_count', 'medium_count', 'low_count',
            'report_url', 'error_message', 'findings_summary',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_findings_summary(self, obj):
        return {
            'total': obj.findings_count,
            'critical': obj.critical_count,
            'high': obj.high_count,
            'medium': obj.medium_count,
            'low': obj.low_count,
        }


class ScanDetailSerializer(ScanSerializer):
    """
    Detailed serializer for Scan with findings.
    """
    findings = FindingSerializer(many=True, read_only=True)
    
    class Meta(ScanSerializer.Meta):
        fields = ScanSerializer.Meta.fields + ['findings', 'raw_results']


class SecurityAnalysisSerializer(serializers.ModelSerializer):
    """
    Serializer for SecurityAnalysis model.
    """
    analyst_name = serializers.CharField(source='analyst.username', read_only=True)
    change_request_id = serializers.CharField(source='change_request.external_id', read_only=True)
    scans_count = serializers.SerializerMethodField()
    
    class Meta:
        model = SecurityAnalysis
        fields = [
            'id', 'change_request', 'change_request_id', 'analyst', 'analyst_name',
            'status', 'started_at', 'completed_at', 'notes', 'risk_score',
            'scans_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'analyst', 'created_at', 'updated_at']
    
    def get_scans_count(self, obj):
        return obj.scans.count()


class SecurityAnalysisDetailSerializer(SecurityAnalysisSerializer):
    """
    Detailed serializer for SecurityAnalysis with scans.
    """
    scans = ScanSerializer(many=True, read_only=True)
    
    class Meta(SecurityAnalysisSerializer.Meta):
        fields = SecurityAnalysisSerializer.Meta.fields + ['scans']
