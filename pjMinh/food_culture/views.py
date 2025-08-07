from django.shortcuts import render, get_object_or_404
from .models import TraditionalFood, Ingredient, OrderingPhrase, CulturalTip

# Create your views here.

def food_list(request):
    """Danh sách các món ăn truyền thống"""
    foods = TraditionalFood.objects.filter(is_active=True)
    return render(request, 'food_culture/food_list.html', {
        'foods': foods
    })

def food_detail(request, food_id):
    """Chi tiết món ăn với nguyên liệu, cách gọi món và mẹo văn hóa"""
    food = get_object_or_404(TraditionalFood, id=food_id, is_active=True)
    ingredients = food.ingredients.all()
    ordering_phrases = food.ordering_phrases.all()
    cultural_tips = food.cultural_tips.all()
    
    # Phân loại mẹo văn hóa theo danh mục
    tips_by_category = {}
    for tip in cultural_tips:
        if tip.category not in tips_by_category:
            tips_by_category[tip.category] = []
        tips_by_category[tip.category].append(tip)
    
    return render(request, 'food_culture/food_detail.html', {
        'food': food,
        'ingredients': ingredients,
        'ordering_phrases': ordering_phrases,
        'tips_by_category': tips_by_category
    })

def food_by_region(request, region):
    """Lọc món ăn theo vùng miền"""
    foods = TraditionalFood.objects.filter(region__icontains=region, is_active=True)
    return render(request, 'food_culture/food_list.html', {
        'foods': foods,
        'region': region
    })

def cultural_tips(request):
    """Trang tổng hợp các mẹo văn hóa"""
    tips = CulturalTip.objects.all()
    tips_by_category = {}
    for tip in tips:
        if tip.category not in tips_by_category:
            tips_by_category[tip.category] = []
        tips_by_category[tip.category].append(tip)
    
    return render(request, 'food_culture/cultural_tips.html', {
        'tips_by_category': tips_by_category
    })

def allergen_info(request):
    """Thông tin về các nguyên liệu gây dị ứng"""
    allergens = Ingredient.objects.filter(is_allergen=True)
    return render(request, 'food_culture/allergen_info.html', {
        'allergens': allergens
    })
