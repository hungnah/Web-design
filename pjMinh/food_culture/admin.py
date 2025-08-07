from django.contrib import admin
from .models import TraditionalFood, Ingredient, OrderingPhrase, CulturalTip, FoodLink

@admin.register(TraditionalFood)
class TraditionalFoodAdmin(admin.ModelAdmin):
    list_display = ['name', 'region', 'difficulty_level', 'is_active', 'ingredient_count']
    list_filter = ['region', 'difficulty_level', 'is_active']
    search_fields = ['name', 'vietnamese_name', 'english_name']
    
    def ingredient_count(self, obj):
        return obj.ingredients.count()
    ingredient_count.short_description = 'Số nguyên liệu'

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'food', 'is_allergen', 'english_name']
    list_filter = ['is_allergen', 'food__region']
    search_fields = ['name', 'english_name']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('food')

@admin.register(OrderingPhrase)
class OrderingPhraseAdmin(admin.ModelAdmin):
    list_display = ['vietnamese', 'english', 'food', 'order']
    list_filter = ['food__region']
    search_fields = ['vietnamese', 'english']
    ordering = ['food', 'order']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('food')

@admin.register(CulturalTip)
class CulturalTipAdmin(admin.ModelAdmin):
    list_display = ['title', 'food', 'category', 'order']
    list_filter = ['category', 'food__region']
    search_fields = ['title', 'content']
    ordering = ['food', 'order']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('food')

@admin.register(FoodLink)
class FoodLinkAdmin(admin.ModelAdmin):
    list_display = ['keyword', 'food', 'lesson']
    list_filter = ['food__region']
    search_fields = ['keyword', 'food__name']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('food', 'lesson')
