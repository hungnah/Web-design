from django.contrib import admin
from .models import Evaluation

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ['evaluator', 'evaluatee', 'score', 'created_at']
    list_filter = ['score', 'created_at']
    search_fields = ['evaluator__username', 'evaluatee__username', 'comment']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
