from django.db import models

class CodeReview(models.Model):
    """Model to store code review results"""
    code = models.TextField()
    language = models.CharField(max_length=50, default='python')
    complexity_score = models.FloatField(null=True, blank=True)
    ai_feedback = models.TextField(blank=True)
    issues_found = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Review {self.id} - {self.language} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"