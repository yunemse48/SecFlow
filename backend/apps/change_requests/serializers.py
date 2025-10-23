"""
Serializers for change requests app.
"""

from rest_framework import serializers
from .models import ChangeRequest, ChangeRequestComment, ChangeRequestAttachment


class ChangeRequestCommentSerializer(serializers.ModelSerializer):
    """
    Serializer for ChangeRequestComment model.
    """
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = ChangeRequestComment
        fields = [
            'id', 'change_request', 'user', 'user_name', 'content',
            'is_internal', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class ChangeRequestAttachmentSerializer(serializers.ModelSerializer):
    """
    Serializer for ChangeRequestAttachment model.
    """
    uploaded_by_name = serializers.CharField(source='uploaded_by.username', read_only=True)
    
    class Meta:
        model = ChangeRequestAttachment
        fields = [
            'id', 'change_request', 'file', 'filename', 'file_size',
            'uploaded_by', 'uploaded_by_name', 'created_at'
        ]
        read_only_fields = ['id', 'uploaded_by', 'file_size', 'created_at']


class ChangeRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for ChangeRequest model.
    """
    assigned_to_name = serializers.CharField(source='assigned_to.username', read_only=True)
    comments_count = serializers.SerializerMethodField()
    attachments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ChangeRequest
        fields = [
            'id', 'external_id', 'source', 'title', 'description',
            'status', 'priority', 'requester', 'assigned_to', 'assigned_to_name',
            'repository_url', 'branch_name', 'pull_request_url', 'jenkins_build_url',
            'external_data', 'requested_date', 'due_date', 'completed_date',
            'comments_count', 'attachments_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def get_attachments_count(self, obj):
        return obj.attachments.count()


class ChangeRequestDetailSerializer(ChangeRequestSerializer):
    """
    Detailed serializer for ChangeRequest with nested relations.
    """
    comments = ChangeRequestCommentSerializer(many=True, read_only=True)
    attachments = ChangeRequestAttachmentSerializer(many=True, read_only=True)
    
    class Meta(ChangeRequestSerializer.Meta):
        fields = ChangeRequestSerializer.Meta.fields + ['comments', 'attachments']
