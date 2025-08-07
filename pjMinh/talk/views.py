from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Topic, Lesson, Sentence, MiniGame, UserGoal
from food_culture.models import FoodLink

def home(request):
    """Trang chủ với lựa chọn mục tiêu"""
    goals = UserGoal.objects.all()
    topics = Topic.objects.filter(is_active=True)
    return render(request, 'talk/home.html', {
        'goals': goals,
        'topics': topics
    })

def topic_list(request):
    """Danh sách các chủ đề"""
    topics = Topic.objects.filter(is_active=True)
    return render(request, 'talk/topic_list.html', {
        'topics': topics
    })

def topic_detail(request, topic_id):
    """Chi tiết chủ đề và danh sách bài học"""
    topic = get_object_or_404(Topic, id=topic_id, is_active=True)
    lessons = topic.lessons.filter(is_active=True)
    return render(request, 'talk/topic_detail.html', {
        'topic': topic,
        'lessons': lessons
    })

def lesson_detail(request, topic_id, lesson_id):
    """Chi tiết bài học với mẫu câu và mini game"""
    topic = get_object_or_404(Topic, id=topic_id, is_active=True)
    lesson = get_object_or_404(Lesson, id=lesson_id, topic=topic, is_active=True)
    sentences = lesson.sentences.all()
    minigames = lesson.minigames.all()
    
    # Tìm các liên kết món ăn trong bài học
    food_links = FoodLink.objects.filter(lesson=lesson)
    
    return render(request, 'talk/lesson_detail.html', {
        'topic': topic,
        'lesson': lesson,
        'sentences': sentences,
        'minigames': minigames,
        'food_links': food_links
    })

def minigame_play(request, game_id):
    """Chơi mini game"""
    game = get_object_or_404(MiniGame, id=game_id)
    return render(request, 'talk/minigame_play.html', {
        'game': game
    })

def minigame_data(request, game_id):
    """API trả về dữ liệu mini game"""
    game = get_object_or_404(MiniGame, id=game_id)
    return JsonResponse({
        'id': game.id,
        'title': game.title,
        'type': game.game_type,
        'content': game.content,
        'instructions': game.instructions
    })

def search_food_link(request):
    """Tìm kiếm liên kết món ăn từ từ khóa"""
    keyword = request.GET.get('keyword', '')
    if keyword:
        food_links = FoodLink.objects.filter(keyword__icontains=keyword)
        return JsonResponse({
            'links': [{
                'keyword': link.keyword,
                'food_name': link.food.name,
                'food_url': link.food.get_absolute_url()
            } for link in food_links]
        })
    return JsonResponse({'links': []})
