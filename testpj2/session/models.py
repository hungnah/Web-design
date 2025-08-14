from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Evaluation(models.Model):
    """
    Evaluation model for storing user ratings after language exchange sessions
    """
    evaluator = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='given_evaluations',
        help_text="User who gave the evaluation"
    )
    evaluatee = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='received_evaluations',
        help_text="User who received the evaluation"
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Rating score from 1 to 10"
    )
    comment = models.TextField(blank=True, help_text="Optional comment about the session")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['evaluator', 'evaluatee']  # One evaluation per user pair
        
    def __str__(self):
        return f"{self.evaluator.username} → {self.evaluatee.username}: {self.score}/10"
