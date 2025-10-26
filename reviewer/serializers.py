from rest_framework import serializers
from .models import CodeReview

class CodeReviewSerializer(serializers.ModelSerializer):
    #Serializer for code review requests and responses
    
    class Meta:
        model = CodeReview
        fields = ['id', 'code', 'language', 'complexity_score', 
                  'ai_feedback', 'issues_found', 'created_at']
        read_only_fields = ['id', 'complexity_score', 'ai_feedback', 
                           'issues_found', 'created_at']

class CodeSubmissionSerializer(serializers.Serializer):
    #Serializer for code submission
    code = serializers.CharField()
    language = serializers.CharField(default='python')
    use_ai = serializers.BooleanField(default=True)