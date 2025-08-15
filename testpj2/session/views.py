import os
import re
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from user_profile.models import CustomUser
from event_creation.models import LanguageExchangePost
from django.shortcuts import render
from django.contrib import messages

"""
Session Views for Language Exchange Platform

This module handles session management including:
- Study sessions with language exchange partners
- Session evaluation and rating
- Gender and user information display for better user experience

Features:
- Displays gender, nationality, and city information of the person who posted
- Supports both Japanese and Vietnamese users
- Includes error handling and logging for debugging
"""

def study(request, partner_id, post_id, phrase_id):
    timer_flag = request.GET.get('timer') == '1'
    
    # Ensure phrase_id is within valid range (1-10) for template selection
    # If phrase_id is larger than 10, it's likely a database ID, so we'll map it to a lesson template
    if phrase_id > 10:
        # Map large phrase_id to lesson template number (1-10)
        # This handles cases where phrase_id comes from database instead of lesson number
        lesson_number = ((phrase_id - 1) % 10) + 1
    else:
        lesson_number = phrase_id
    
    template_name = f'session/study_{lesson_number}.html'
    
    # Get the language exchange post to access user information
    poster = None
    try:
        post = LanguageExchangePost.objects.get(id=post_id)
        # Determine which user posted this (japanese_user or vietnamese_user)
        if post.japanese_user and post.japanese_user.id == int(partner_id):
            poster = post.japanese_user
        elif post.vietnamese_user and post.vietnamese_user.id == int(partner_id):
            poster = post.vietnamese_user
        else:
            # Log this case for debugging
            print(f"Warning: partner_id {partner_id} not found in post {post_id}")
    except LanguageExchangePost.DoesNotExist:
        print(f"Error: LanguageExchangePost with id {post_id} not found")
    except Exception as e:
        print(f"Error in study view: {e}")
    
    context = {
        'partner_id': partner_id,
        'post_id': post_id,
        'phrase_id': phrase_id,
        'lesson_number': lesson_number,
        'timer_flag': timer_flag,
        'poster_gender': poster.gender if poster else None,
        'poster_nationality': poster.nationality if poster else None,
        'poster_city': poster.city if poster else None,
        'poster': poster,
    }
    return render(request, template_name, context)

def evaluate(request, partner_id, post_id, phrase_id):
    score_range = range(1, 11)  # 1〜10
    
    # Ensure phrase_id is within valid range (1-10) for template selection
    # If phrase_id is larger than 10, it's likely a database ID, so we'll map it to a lesson template
    if phrase_id > 10:
        # Map large phrase_id to lesson template number (1-10)
        # This handles cases where phrase_id comes from database instead of lesson number
        lesson_number = ((phrase_id - 1) % 10) + 1
    else:
        lesson_number = phrase_id
    
    # Get the language exchange post to access user information
    poster = None
    try:
        post = LanguageExchangePost.objects.get(id=post_id)
        # Determine which user posted this (japanese_user or vietnamese_user)
        if post.japanese_user and post.japanese_user.id == int(partner_id):
            poster = post.japanese_user
        elif post.vietnamese_user and post.vietnamese_user.id == int(partner_id):
            poster = post.vietnamese_user
        else:
            # Log this case for debugging
            print(f"Warning: partner_id {partner_id} not found in post {post_id}")
    except LanguageExchangePost.DoesNotExist:
        print(f"Error: LanguageExchangePost with id {post_id} not found")
    except Exception as e:
        print(f"Error in evaluate view: {e}")
    
    context = {
        'partner_id': partner_id,
        'post_id': post_id,
        'phrase_id': phrase_id,
        'lesson_number': lesson_number,
        'score_range': score_range,
        'poster_gender': poster.gender if poster else None,
        'poster_nationality': poster.nationality if poster else None,
        'poster_city': poster.city if poster else None,
        'poster': poster,
    }
    return render(request, 'session/evaluate.html', context)

@require_POST
@login_required
def submit_evaluation(request):
    partner_id = request.POST.get('partner_id')
    score = request.POST.get('score')
    comment = request.POST.get('comment', '')

    if not partner_id or not score:
        # 必要な情報がない場合はエラーハンドリング
        return redirect('/some-error-page/')

    try:
        score = int(score)
    except ValueError:
        # scoreが数字でない場合のエラーハンドリング
        return redirect('/some-error-page/')

    partner = get_object_or_404(CustomUser, id=partner_id)
    post_id = request.POST.get("post_id")
    post = get_object_or_404(LanguageExchangePost, id=post_id)

    # Save evaluation to database
    from .models import Evaluation
    evaluation, created = Evaluation.objects.get_or_create(
        evaluator=request.user,
        evaluatee=partner,
        defaults={'score': score, 'comment': comment}
    )
    
    if not created:
        # Update existing evaluation
        evaluation.score = score
        evaluation.comment = comment
        evaluation.save()

    # セッションを完了
    post.status = 'completed'
    post.save()

    # 評価後のリダイレクト先(例：ダッシュボード)
    return redirect('/auth/dashboard/')

def list(request):
    template_dir = os.path.join(settings.BASE_DIR, 'templates', 'session')

    pattern = re.compile(r'^study_(\d+)\.html$')
    study_files = []

    for fname in os.listdir(template_dir):
        if pattern.match(fname):
            study_files.append(fname)

    study_files.sort(key=lambda x: int(pattern.match(x).group(1)))

    context = {'study_files': study_files}
    return render(request, 'session/list.html', context)

def study_detail(request, phrase_id):
    # Create a mapping between phrase IDs and lesson content
    # This maps database phrase IDs to the 10 structured lessons
    lesson_mapping = {
        1: {
            'title': '＜１＞lời chào\n「挨拶」を学ぼう',
            'messages': [
                {'side': 'system', 'text': '＜１＞lời chào\n「挨拶」を学ぼう'},
                {'side': 'left', 'text': 'Xin chào.\n(こんにちは)'},
                {'side': 'right', 'text': 'Xin chào.\n(こんにちは)'},
                {'side': 'system', 'text': '＜２＞TÔI\n「私」を学ぼう'},
                {'side': 'left', 'text': 'Lặp lại theo tôi.\n(私が読んだ後に繰り返してください)'},
                {'side': 'left', 'text': 'Tôi là Minh.\n(私はMinhです。)'},
                {'side': 'right', 'text': 'Tôi là Minh.\n(私はMinhです。)'},
                {'side': 'left', 'text': 'Tôi là Hayato.\n(私はHayatoです。)'},
                {'side': 'right', 'text': 'Tôi là Hayato.\n(私はHayatoです。)'},
                {'side': 'left', 'text': 'Tôi là giáo viên.\n(私は先生です。)'},
                {'side': 'right', 'text': 'Tôi là giáo viên.\n(私は先生です。)'},
                {'side': 'left', 'text': 'Tôi là học sinh.\n(私は学生です。)'},
                {'side': 'right', 'text': 'Tôi là học sinh.\n(私は学生です。)'},
                {'side': 'left', 'text': 'Tôi là người Việt Nam.\n(私はベトナム人です。)'},
                {'side': 'right', 'text': 'Tôi là người Việt Nam.\n(私はベトナム人です。)'},
                {'side': 'left', 'text': 'Tôi là người Nhật.\n(私は日本人です。)'},
                {'side': 'right', 'text': 'Tôi là người Nhật.\n(私は日本人です。)'},
                {'side': 'system', 'text': '＜３＞Bạn\n「あなた」を学ぼう'},
                {'side': 'left', 'text': 'Lặp lại theo tôi.\n(私が読んだ後に繰り返してください)'},
                {'side': 'left', 'text': 'Bạn là Minh.\n(あなたはMinhです。)'},
                {'side': 'right', 'text': 'Bạn là Minh.\n(あなたはMinhです。)'},
                {'side': 'left', 'text': 'Bạn là Hayato.\n(あなたはHayatoです。)'},
                {'side': 'right', 'text': 'Bạn là Hayato.\n(あなたはHayatoです。)'},
                {'side': 'left', 'text': 'Bạn là giáo viên.\n(あなたは先生ですか？)'},
                {'side': 'right', 'text': 'Bạn là giáo viên.\n(あなたは先生ですか？)'},
                {'side': 'left', 'text': 'Bạn là học sinh.\n(あなたは学生ですか？)'},
                {'side': 'right', 'text': 'Bạn là học sinh.\n(あなたは学生ですか？)'},
                {'side': 'left', 'text': 'Bạn là người Việt Nam.\n(あなたはベトナム人ですか？)'},
                {'side': 'right', 'text': 'Bạn là người Việt Nam.\n(あなたはベトナム人ですか？)'},
                {'side': 'left', 'text': 'Bạn là người Nhật.\n(あなたは日本人ですか？)'},
                {'side': 'right', 'text': 'Bạn là người Nhật.\n(あなたは日本人ですか？)'},
                {'side': 'system', 'text': '＜４＞Bạn có phải\n「あなたは～ですか？」を学ぼう'},
                {'side': 'left', 'text': 'Lặp lại theo tôi.\n(私が読んだ後に繰り返してください)'},
                {'side': 'left', 'text': 'Bạn có phải là Minh？\n(あなたはMinhですか？)'},
                {'side': 'right', 'text': 'Bạn có phải là Minh？\n(あなたはMinhですか？)'},
                {'side': 'left', 'text': 'Bạn có phải là Hayato？\n(あなたはHayatoですか？)'},
                {'side': 'right', 'text': 'Bạn có phải là Hayato？\n(あなたはHayatoですか？)'},
                {'side': 'left', 'text': 'Bạn có phải là giáo viên？\n(あなたは先生ですか？)'},
                {'side': 'right', 'text': 'Bạn có phải là giáo viên？\n(あなたは先生ですか？)'},
                {'side': 'left', 'text': 'Bạn có phải là học sinh？\n(あなたは学生ですか？)'},
                {'side': 'right', 'text': 'Bạn có phải là học sinh？\n(あなたは学生ですか？)'},
                {'side': 'left', 'text': 'Bạn có phải là người Việt Nam？\n(あなたはベトナム人ですか？)'},
                {'side': 'right', 'text': 'Bạn có phải là người Việt Nam？\n(あなたはベトナム人ですか？)'},
                {'side': 'left', 'text': 'Bạn có phải là người Nhật？\n(あなたは日本人ですか？)'},
                {'side': 'right', 'text': 'Bạn có phải là người Nhật？\n(あなたは日本人ですか？)'},
                {'side': 'system', 'text': '＜５＞Vâng・Không\n「はい・いいえ」を学ぼう'},
                {'side': 'left', 'text': 'Bạn có phải là Hayato？\n(あなたはHayatoですか？)'},
                {'side': 'right', 'text': 'Bạn có phải là Hayato？\n(あなたはHayatoですか？)'},
                {'side': 'left', 'text': 'Vâng, tôi là Hayato.\n(はい、私はHayatoです。)'},
                {'side': 'right', 'text': 'Vâng, tôi là Hayato.\n(はい、私はHayatoです。)'},
                {'side': 'left', 'text': 'Không, tôi là Minh.\n(いいえ、私はMinhです。)'},
                {'side': 'right', 'text': 'Không, tôi là Minh.\n(いいえ、私はMinhです。)'},
                {'side': 'left', 'text': 'Bạn có phải là học sinh？\n(あなたは学生ですか？)'},
                {'side': 'right', 'text': 'Bạn có phải là học sinh？\n(あなたは学生ですか？)'},
                {'side': 'left', 'text': 'Vâng, tôi là học sinh.\n(はい、私は学生です。)'},
                {'side': 'right', 'text': 'Vâng, tôi là học sinh.\n(はい、私は学生です。)'},
                {'side': 'left', 'text': 'Không, tôi là giáo viên.\n(いいえ、私は先生です。)'},
                {'side': 'right', 'text': 'Không, tôi là giáo viên.\n(いいえ、私は先生です。)'},
                {'side': 'left', 'text': 'Bạn có phải là người Nhật？\n(あなたは日本人ですか？)'},
                {'side': 'right', 'text': 'Bạn có phải là người Nhật？\n(あなたは日本人ですか？)'},
                {'side': 'left', 'text': 'Vâng, tôi là người Nhật.\n(はい、私は日本人です。)'},
                {'side': 'right', 'text': 'Vâng, tôi là người Nhật.\n(はい、私は日本人です。)'},
                {'side': 'left', 'text': 'Không, tôi là người Việt Nam.\n(いいえ、私はベトナム人です。)'},
                {'side': 'right', 'text': 'Không, tôi là người Việt Nam.\n(いいえ、私はベトナム人です。)'},
                {'side': 'system', 'text': '＜６＞trò chuyện①\n学んだ表現を使って会話しよう①'},
                {'side': 'left', 'text': 'Xin chào! Tôi là Minh.\n(こんにちは！私はMinhです。)'},
                {'side': 'right', 'text': 'Xin chào! Tôi là Hayato.\n(こんにちは！私はHayatoです。)'},
                {'side': 'left', 'text': 'Bạn có phải là học sinh？\n(あなたは学生ですか？)'},
                {'side': 'right', 'text': 'Vâng, tôi là học sinh. Bạn có phải là giáo viên？\n(はい、私は学生です。あなたは先生ですか？)'},
                {'side': 'left', 'text': 'Vâng, tôi là giáo viên. Bạn có phải là người Việt Nam？\n(はい、私は先生です。あなたはベトナム人ですか？)'},
                {'side': 'right', 'text': 'Không, tôi là người Nhật. Bạn có phải là người Nhật？\n(いいえ、私は日本人です。あなたは日本人ですか？)'},
                {'side': 'left', 'text': 'Không, tôi là người Việt Nam.\n(いいえ、私はベトナム人です。)'},
                {'side': 'system', 'text': '＜６＞trò chuyện②\n学んだ表現を使って会話しよう②'},
                {'side': 'right', 'text': 'Xin chào! Tôi là Minh.\n(こんにちは！私はMinhです。)'},
                {'side': 'left', 'text': 'Xin chào! Tôi là Hayato.\n(こんにちは！私はHayatoです。)'},
                {'side': 'right', 'text': 'Bạn có phải là học sinh？\n(あなたは学生ですか？)'},
                {'side': 'left', 'text': 'Vâng, tôi là học sinh. Bạn có phải là giáo viên？\n(はい、私は学生です。あなたは先生ですか？)'},
                {'side': 'right', 'text': 'Vâng, tôi là giáo viên. Bạn có phải là người Việt Nam？\n(はい、私は先生です。あなたはベトナム人ですか？)'},
                {'side': 'left', 'text': 'Không, tôi là người Nhật. Bạn có phải là người Nhật？\n(いいえ、私は日本人です。あなたは日本人ですか？)'},
                {'side': 'right', 'text': 'Không, tôi là người Việt Nam.\n(いいえ、私はベトナム人です。)'},
            ]
        },
        2: {
            'title': '＜２＞Chào buổi sáng\n「おはよう」を学ぼう',
            'messages': [
                {'side': 'system', 'text': '＜２＞Chào buổi sáng\n「おはよう」を学ぼう'},
                {'side': 'left', 'text': 'Chào buổi sáng.\n(おはようございます。)'},
                {'side': 'right', 'text': 'Chào buổi sáng.\n(おはようございます。)'},
                {'side': 'left', 'text': 'Chào nhé! (thân mật)\n(おはよう。)'},
                {'side': 'right', 'text': 'Chào nhé! (thân mật)\n(おはよう。)'},
                {'side': 'left', 'text': 'Chúc bạn một ngày tốt lành.\n(良い一日を。)'},
                {'side': 'right', 'text': 'Cảm ơn. Bạn cũng vậy nhé.\n(ありがとうございます。あなたも良い一日を。)'},
                {'side': 'system', 'text': '＜練習＞　Lặp lại và đối thoại ngắn'},
                {'side': 'left', 'text': 'おはようございます。私はMinhです。\n(Chào buổi sáng. Tôi là Minh.)'},
                {'side': 'right', 'text': 'おはようございます。私はHayatoです。\n(Chào buổi sáng. Tôi là Hayato.)'},
            ]
        },
        3: {
            'title': '＜３＞Chào buổi trưa\n「こんにちは」を学ぼう',
            'messages': [
                {'side': 'system', 'text': '＜３＞Chào buổi trưa\n「こんにちは」を学ぼう'},
                {'side': 'left', 'text': 'Chào buổi trưa.\n(こんにちは。)'},
                {'side': 'right', 'text': 'Chào buổi trưa.\n(こんにちは。)'},
                {'side': 'left', 'text': 'Bạn đã ăn trưa chưa？\n(もうお昼ご飯を食べましたか？)'},
                {'side': 'right', 'text': 'Chưa, mình định đi ăn bây giờ.\n(まだです。これから食べに行く予定です。)'},
                {'side': 'left', 'text': 'Chúc bữa trưa vui vẻ.\n(良いお昼を。)'},
                {'side': 'right', 'text': 'Cảm ơn bạn.\n(ありがとうございます。)'},
            ]
        },
        4: {
            'title': '＜４＞Chào buổi tối\n「こんばんは」を学ぼう',
            'messages': [
                {'side': 'system', 'text': '＜４＞Chào buổi tối\n「こんばんは」を学ぼう'},
                {'side': 'left', 'text': 'Chào buổi tối.\n(こんばんは。)'},
                {'side': 'right', 'text': 'Chào buổi tối.\n(こんばんは。)'},
                {'side': 'left', 'text': 'Bạn đã ăn tối chưa？\n(もう夕食を食べましたか？)'},
                {'side': 'right', 'text': 'Rồi, mình đã ăn rồi.\n(はい、もう食べました。)'},
                {'side': 'left', 'text': 'Chúc ngủ ngon sau nhé.\n(おやすみなさい。)'},
                {'side': 'right', 'text': 'Ngủ ngon nhé.\n(おやすみなさい。)'},
            ]
        },
        5: {
            'title': '＜５＞Bạn khỏe không\n「お元気ですか？」を学ぼう',
            'messages': [
                {'side': 'system', 'text': '＜５＞Bạn khỏe không\n「お元気ですか？」を学ぼう'},
                {'side': 'left', 'text': 'Bạn khỏe không?\n(お元気ですか？)'},
                {'side': 'right', 'text': 'Bạn khỏe không?\n(お元気ですか？)'},
                {'side': 'left', 'text': 'Hôm nay bạn có khỏe không?\n(今日はお元気ですか？)'},
                {'side': 'right', 'text': 'Tôi hơi mệt nhưng ổn.\n(少し疲れていますが、大丈夫です。)'},
                {'side': 'left', 'text': 'Bạn có cần nghỉ không?\n(休んだ方がいいですか？)'},
                {'side': 'right', 'text': 'Không, cảm ơn. Tôi ổn.\n(いいえ、大丈夫です。ありがとう。)'},
            ]
        },
        6: {
            'title': '＜６＞Tôi khỏe, cảm ơn\n「元気です、ありがとう」を学ぼう',
            'messages': [
                {'side': 'system', 'text': '＜６＞Tôi khỏe, cảm ơn\n「元気です、ありがとう」を学ぼう'},
                {'side': 'left', 'text': 'Tôi khỏe, cảm ơn.\n(元気です、ありがとう。)'},
                {'side': 'right', 'text': 'Tôi khỏe, cảm ơn.\n(元気です、ありがとう。)'},
                {'side': 'left', 'text': 'Rất vui khi nghe vậy.\n(それは良かったです。)'},
                {'side': 'right', 'text': 'Cảm ơn bạn.\n(ありがとうございます。)'},
                {'side': 'left', 'text': 'Nếu mệt thì hãy nghỉ nhé.\n(疲れたら休んでくださいね。)'},
            ]
        },
        7: {
            'title': '＜７＞Cảm ơn và xin lỗi\n「ありがとうとごめんなさい」を学ぼう',
            'messages': [
                {'side': 'system', 'text': '＜７＞Cảm ơn và xin lỗi\n「ありがとうとごめんなさい」を学ぼう'},
                {'side': 'left', 'text': 'Cảm ơn bạn.\n(ありがとうございます。)'},
                {'side': 'right', 'text': 'Không có gì.\n(どういたしまして。)'},
                {'side': 'left', 'text': 'Xin lỗi, tôi đến muộn.\n(すみません、遅刻しました。)'},
                {'side': 'right', 'text': 'Không sao đâu.\n(大丈夫です。)'},
                {'side': 'left', 'text': 'Cảm ơn bạn đã hiểu.\n(理解していただき、ありがとうございます。)'},
                {'side': 'right', 'text': 'Rất vui được giúp bạn.\n(お手伝いできて嬉しいです。)'},
            ]
        },
        8: {
            'title': '＜８＞Số đếm cơ bản\n「基本的な数字」を学ぼう',
            'messages': [
                {'side': 'system', 'text': '＜８＞Số đếm cơ bản\n「基本的な数字」を学ぼう'},
                {'side': 'left', 'text': 'Một, hai, ba, bốn, năm.\n(一、二、三、四、五。)'},
                {'side': 'right', 'text': 'Một, hai, ba, bốn, năm.\n(一、二、三、四、五。)'},
                {'side': 'left', 'text': 'Sáu, bảy, tám, chín, mười.\n(六、七、八、九、十。)'},
                {'side': 'right', 'text': 'Sáu, bảy, tám, chín, mười.\n(六、七、八、九、十。)'},
                {'side': 'left', 'text': 'Bạn có thể đếm từ 1 đến 10 không?\n(1から10まで数えられますか？)'},
                {'side': 'right', 'text': 'Vâng, tôi có thể.\n(はい、できます。)'},
            ]
        },
        9: {
            'title': '＜９＞Màu sắc\n「色」を学ぼう',
            'messages': [
                {'side': 'system', 'text': '＜９＞Màu sắc\n「色」を学ぼう'},
                {'side': 'left', 'text': 'Màu đỏ, màu xanh, màu vàng.\n(赤、青、黄。)'},
                {'side': 'right', 'text': 'Màu đỏ, màu xanh, màu vàng.\n(赤、青、黄。)'},
                {'side': 'left', 'text': 'Màu trắng, màu đen, màu tím.\n(白、黒、紫。)'},
                {'side': 'right', 'text': 'Màu trắng, màu đen, màu tím.\n(白、黒、紫。)'},
                {'side': 'left', 'text': 'Bạn thích màu gì?\n(何色が好きですか？)'},
                {'side': 'right', 'text': 'Tôi thích màu xanh.\n(青が好きです。)'},
            ]
        },
        10: {
            'title': '＜１０＞Thời tiết\n「天気」を学ぼう',
            'messages': [
                {'side': 'system', 'text': '＜１０＞Thời tiết\n「天気」を学ぼう'},
                {'side': 'left', 'text': 'Hôm nay trời đẹp.\n(今日は天気が良いです。)'},
                {'side': 'right', 'text': 'Vâng, trời rất đẹp.\n(はい、とても良い天気です。)'},
                {'side': 'left', 'text': 'Ngày mai có mưa không?\n(明日は雨ですか？)'},
                {'side': 'right', 'text': 'Có thể, tôi không chắc chắn.\n(かもしれません、確実ではありません。)'},
                {'side': 'left', 'text': 'Chúc bạn một ngày tốt lành.\n(良い一日を。)'},
                {'side': 'right', 'text': 'Cảm ơn, bạn cũng vậy.\n(ありがとう、あなたも。)'},
            ]
        }
    }
    
    # Map phrase_id to lesson number (1-10)
    # This creates a mapping between database phrase IDs and lesson numbers
    lesson_number = ((phrase_id - 1) % 10) + 1
    
    # Get the lesson content
    lesson = lesson_mapping.get(lesson_number, lesson_mapping[1])  # Default to lesson 1 if not found
    
    context = {
        'messages': lesson['messages'],
        'left_icon': 'images/session/teacher.png',
        'left_name': '先生/giáo viên',
        'right_icon': 'images/session/student.png',
        'right_name': '生徒/học sinh',
        'lesson_title': lesson['title'],
    }
    return render(request, 'session/study.html', context)


def text_session(request, post_id):
    """
    Simple two-step text session flow:
    step=1: show Japanese Learning phrases
    step=2: show Vietnamese Learning phrases
    """
    step_param = request.GET.get('step', '1')
    try:
        step = int(step_param)
    except ValueError:
        step = 1

    post = get_object_or_404(LanguageExchangePost, id=post_id)

    # Determine content based on learning phrases
    if step == 1:
        content_title = 'Các câu nói muốn học (Japanese Learning)'
        if post.japanese_learning_phrases.exists():
            phrases = post.japanese_learning_phrases.all()
            content_text = '\n'.join([f"• {phrase.vietnamese_text} ({phrase.get_category_display()})" for phrase in phrases])
        else:
            content_text = 'Không có câu nói nào được chọn'
        # Chuyển thẳng sang chat room thay vì bước 2
        next_url = f"/session/start-chat/{post.id}/"
        next_label = 'Bắt đầu chat'
        is_final = False
    else:
        content_title = 'Các câu nói muốn học (Vietnamese Learning)'
        if post.vietnamese_learning_phrases.exists():
            phrases = post.vietnamese_learning_phrases.all()
            content_text = '\n'.join([f"• {phrase.vietnamese_text} ({phrase.get_category_display()})" for phrase in phrases])
        else:
            content_text = 'Không có câu nói nào được chọn'
        next_url = '/auth/dashboard/'
        next_label = 'Kết thúc phiên học'
        is_final = True

    context = {
        'post': post,
        'step': step,
        'content_title': content_title,
        'content_text': content_text,
        'next_url': next_url,
        'next_label': next_label,
        'is_final': is_final,
    }

    return render(request, 'session/text_session.html', context)


@login_required
def start_chat_session(request, post_id):
    """
    Start chat session by creating/accessing chat room and redirecting to chat
    """
    post = get_object_or_404(LanguageExchangePost, id=post_id)
    
    # Check if user has access to this post
    if request.user not in [post.japanese_user, post.vietnamese_user]:
        messages.error(request, 'Bạn không có quyền truy cập vào phiên học này.')
        return redirect('/auth/dashboard/')
    
    # Import ChatRoom here to avoid circular imports
    from chat_system.models import ChatRoom
    
    # Get or create chat room for this post
    chat_room, created = ChatRoom.objects.get_or_create(
        post=post,
        defaults={'is_active': True}
    )
    
    # Redirect to chat room
    return redirect(f'/chat/chat/{chat_room.id}/')

@login_required
def start_learning_session(request, partner_id, post_id, phrase_id):
    """
    Start learning session with conversation based on selected phrase
    This replaces the old study view with dynamic conversation content
    """
    # Get the language exchange post to access user information
    poster = None
    try:
        post = LanguageExchangePost.objects.get(id=post_id)
        # Determine which user posted this (japanese_user or vietnamese_user)
        if post.japanese_user and post.japanese_user.id == int(partner_id):
            poster = post.japanese_user
        elif post.vietnamese_user and post.vietnamese_user.id == int(partner_id):
            poster = post.vietnamese_user
        else:
            # Log this case for debugging
            print(f"Warning: partner_id {partner_id} not found in post {post_id}")
    except LanguageExchangePost.DoesNotExist:
        print(f"Error: LanguageExchangePost with id {post_id} not found")
        return redirect('/auth/dashboard/')
    except Exception as e:
        print(f"Error in start_learning_session view: {e}")
        return redirect('/auth/dashboard/')
    
    # Get the appropriate phrase based on user nationality and what they want to learn
    phrase = None
    
    # Debug logging
    print(f"DEBUG: User nationality: {request.user.nationality}")
    print(f"DEBUG: User ID: {request.user.id}")
    print(f"DEBUG: User username: {request.user.username}")
    print(f"DEBUG: Post ID: {post_id}")
    print(f"DEBUG: Post phrase: {post.phrase}")
    print(f"DEBUG: Post accepted_phrase: {post.accepted_phrase}")
    print(f"DEBUG: Post japanese_learning_phrases count: {post.japanese_learning_phrases.count()}")
    print(f"DEBUG: Post vietnamese_learning_phrases count: {post.vietnamese_learning_phrases.count()}")
    
    # Check if user is authenticated
    if not request.user.is_authenticated:
        print(f"DEBUG: User is not authenticated!")
        return redirect('/auth/login/')
    
    # Check if nationality is set
    if not hasattr(request.user, 'nationality') or not request.user.nationality:
        print(f"DEBUG: User nationality is not set!")
        # Try to get from profile
        try:
            from user_profile.models import CustomUser
            user_profile = CustomUser.objects.get(id=request.user.id)
            print(f"DEBUG: User profile nationality: {user_profile.nationality}")
            request.user.nationality = user_profile.nationality
        except Exception as e:
            print(f"DEBUG: Error getting user profile: {e}")
            request.user.nationality = 'unknown'
    
    if request.user.nationality == 'japanese':
        # Japanese user wants to learn Vietnamese phrases
        print(f"DEBUG: Japanese user - checking japanese_learning_phrases")
        if post.japanese_learning_phrases.exists():
            # Use the first phrase from japanese_learning_phrases, or the accepted_phrase if available
            phrase = post.accepted_phrase if post.accepted_phrase else post.japanese_learning_phrases.first()
            print(f"DEBUG: Japanese user - selected phrase: {phrase}")
        else:
            # Fallback to main phrase
            phrase = post.phrase
            print(f"DEBUG: Japanese user - fallback to main phrase: {phrase}")
    elif request.user.nationality == 'vietnamese':
        # Vietnamese user wants to learn Japanese phrases
        print(f"DEBUG: Vietnamese user - checking vietnamese_learning_phrases")
        if post.vietnamese_learning_phrases.exists():
            # Use the first phrase from vietnamese_learning_phrases, or the accepted_phrase if available
            phrase = post.accepted_phrase if post.accepted_phrase else post.vietnamese_learning_phrases.first()
            print(f"DEBUG: Vietnamese user - selected phrase: {phrase}")
        else:
            # Fallback to main phrase
            phrase = post.phrase
            print(f"DEBUG: Vietnamese user - fallback to main phrase: {phrase}")
    else:
        # Fallback to main phrase for other nationalities
        phrase = post.phrase
        print(f"DEBUG: Other nationality - using main phrase: {phrase}")
    
    # If still no phrase, try to get from the original phrase_id parameter
    if not phrase and phrase_id:
        try:
            from event_creation.models import VietnamesePhrase
            phrase = VietnamesePhrase.objects.get(id=phrase_id)
            print(f"DEBUG: Using phrase_id parameter: {phrase}")
        except Exception as e:
            print(f"DEBUG: Error getting phrase from phrase_id: {e}")
            pass
    
    print(f"DEBUG: Final selected phrase: {phrase}")
    
    # If still no phrase, create a default one
    if not phrase:
        print(f"DEBUG: No phrase found, creating default conversation")
        # Create a default phrase object for fallback
        class DefaultPhrase:
            def __init__(self):
                self.id = 1
                self.vietnamese_text = "Xin chào"
                self.japanese_translation = "こんにちは"
                self.category = "greetings"
                self.difficulty = "beginner"
        
        phrase = DefaultPhrase()
    
    # Determine conversation content based on phrase category and difficulty
    if phrase:
        category = phrase.category
        difficulty = phrase.difficulty
        
        # Generate conversation based on category and difficulty
        if category == 'greetings':
            if difficulty == 'beginner':
                messages = [
                    {'side': 'system', 'text': f'＜{phrase.id}＞{phrase.vietnamese_text}\n「{phrase.japanese_translation}」を学ぼう'},
                    {'side': 'left', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'right', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'left', 'text': 'Lặp lại theo tôi.\n(私が読んだ後に繰り返してください)'},
                    {'side': 'left', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'right', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'system', 'text': '＜練習＞　Lặp lại và đối thoại ngắn'},
                    {'side': 'left', 'text': f'{phrase.japanese_translation}。私は{poster.full_name or poster.username}です。\n({phrase.vietnamese_text}. Tôi là {poster.full_name or poster.username}.)'},
                    {'side': 'right', 'text': f'{phrase.japanese_translation}。私は{request.user.full_name or request.user.username}です。\n({phrase.vietnamese_text}. Tôi là {request.user.full_name or request.user.username}.)'},
                ]
            elif difficulty == 'intermediate':
                messages = [
                    {'side': 'system', 'text': f'＜{phrase.id}＞{phrase.vietnamese_text}\n「{phrase.japanese_translation}」を学ぼう'},
                    {'side': 'left', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'right', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'left', 'text': 'Bạn có thể lặp lại không?\n(繰り返せますか？)'},
                    {'side': 'right', 'text': f'Vâng, {phrase.vietnamese_text}\n(はい、{phrase.japanese_translation})'},
                    {'side': 'left', 'text': 'Rất tốt! Bây giờ hãy thực hành.\n(とても良いです！今度は練習しましょう。)'},
                    {'side': 'system', 'text': '＜会話練習＞'},
                    {'side': 'left', 'text': f'{phrase.japanese_translation}！私は{poster.full_name or poster.username}です。\n({phrase.vietnamese_text}! Tôi là {poster.full_name or poster.username}.)'},
                    {'side': 'right', 'text': f'{phrase.japanese_translation}！Tôi rất vui được gặp bạn.\n({phrase.vietnamese_text}! Rất vui được gặp bạn.)'},
                ]
            else:  # advanced
                messages = [
                    {'side': 'system', 'text': f'＜{phrase.id}＞{phrase.vietnamese_text}\n「{phrase.japanese_translation}」を学ぼう'},
                    {'side': 'left', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'right', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'left', 'text': 'Bạn có thể sử dụng câu này trong tình huống nào?\n(この表現はどんな場面で使えますか？)'},
                    {'side': 'right', 'text': 'Tôi nghĩ có thể dùng khi gặp người mới.\n(新しい人に会った時に使えると思います。)'},
                    {'side': 'left', 'text': 'Đúng rồi! Hãy thực hành với tôi.\n(その通りです！一緒に練習しましょう。)'},
                    {'side': 'system', 'text': '＜応用練習＞'},
                    {'side': 'left', 'text': f'{phrase.japanese_translation}！私は{poster.full_name or poster.username}です。\n({phrase.vietnamese_text}! Tôi là {poster.full_name or poster.username}.)'},
                    {'side': 'right', 'text': f'{phrase.japanese_translation}！Tôi rất vui được gặp bạn. Bạn có khỏe không?\n({phrase.vietnamese_text}! Rất vui được gặp bạn. Bạn có khỏe không?)'},
                ]
        elif category == 'food':
            if difficulty == 'beginner':
                messages = [
                    {'side': 'system', 'text': f'＜{phrase.id}＞{phrase.vietnamese_text}\n「{phrase.japanese_translation}」を学ぼう'},
                    {'side': 'left', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'right', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'left', 'text': 'Đây là câu nói về ẩm thực.\n(これは料理についての表現です。)'},
                    {'side': 'right', 'text': 'Tôi hiểu rồi. Có thể lặp lại không?\n(分かりました。繰り返せますか？)'},
                    {'side': 'left', 'text': f'Vâng, {phrase.vietnamese_text}\n(はい、{phrase.japanese_translation})'},
                    {'side': 'right', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'system', 'text': '＜練習＞　Thực hành về ẩm thực'},
                    {'side': 'left', 'text': f'{phrase.japanese_translation}！Tôi thích món này.\n({phrase.vietnamese_text}! Tôi thích món này.)'},
                    {'side': 'right', 'text': f'{phrase.vietnamese_text}！Tôi cũng thích.\n({phrase.japanese_translation}! Tôi cũng thích.)'},
                ]
            elif difficulty == 'intermediate':
                messages = [
                    {'side': 'system', 'text': f'＜{phrase.id}＞{phrase.vietnamese_text}\n「{phrase.japanese_translation}」を学ぼう'},
                    {'side': 'left', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'right', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'left', 'text': 'Bạn có thể giải thích ý nghĩa không?\n(意味を説明できますか？)'},
                    {'side': 'right', 'text': 'Tôi nghĩ có nghĩa là...\n(意味は...だと思います。)'},
                    {'side': 'left', 'text': 'Rất tốt! Hãy thực hành.\n(とても良いです！練習しましょう。)'},
                    {'side': 'system', 'text': '＜会話練習＞'},
                    {'side': 'left', 'text': f'{phrase.japanese_translation}！Bạn có muốn ăn món này không?\n({phrase.vietnamese_text}! Bạn có muốn ăn món này không?)'},
                    {'side': 'right', 'text': f'{phrase.vietnamese_text}！Vâng, tôi rất muốn.\n({phrase.japanese_translation}! Vâng, tôi rất muốn.)'},
                ]
            else:  # advanced
                messages = [
                    {'side': 'system', 'text': f'＜{phrase.id}＞{phrase.vietnamese_text}\n「{phrase.japanese_translation}」を学ぼう'},
                    {'side': 'left', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'right', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'left', 'text': 'Bạn có thể sử dụng câu này như thế nào?\n(この表現をどう使えますか？)'},
                    {'side': 'right', 'text': 'Tôi nghĩ có thể dùng khi gọi món.\n(料理を注文する時に使えると思います。)'},
                    {'side': 'left', 'text': 'Đúng rồi! Hãy thực hành.\n(その通りです！練習しましょう。)'},
                    {'side': 'system', 'text': '＜応用練習＞'},
                    {'side': 'left', 'text': f'{phrase.japanese_translation}！Tôi muốn gọi món này.\n({phrase.vietnamese_text}! Tôi muốn gọi món này.)'},
                    {'side': 'right', 'text': f'{phrase.vietnamese_text}！Tôi cũng muốn thử.\n({phrase.japanese_translation}! Tôi cũng muốn thử.)'},
                ]
        elif category == 'business':
            if difficulty == 'beginner':
                messages = [
                    {'side': 'system', 'text': f'＜{phrase.id}＞{phrase.vietnamese_text}\n「{phrase.japanese_translation}」を学ぼう'},
                    {'side': 'left', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'right', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'left', 'text': 'Đây là câu nói trong môi trường công việc.\n(これは仕事の場面で使う表現です。)'},
                    {'side': 'right', 'text': 'Tôi hiểu rồi. Có thể lặp lại không?\n(分かりました。繰り返せますか？)'},
                    {'side': 'left', 'text': f'Vâng, {phrase.vietnamese_text}\n(はい、{phrase.japanese_translation})'},
                    {'side': 'right', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                ]
            elif difficulty == 'intermediate':
                messages = [
                    {'side': 'system', 'text': f'＜{phrase.id}＞{phrase.vietnamese_text}\n「{phrase.japanese_translation}」を学ぼう'},
                    {'side': 'left', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'right', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'left', 'text': 'Bạn có thể giải thích ý nghĩa không?\n(意味を説明できますか？)'},
                    {'side': 'right', 'text': 'Tôi nghĩ có nghĩa là...\n(意味は...だと思います。)'},
                    {'side': 'left', 'text': 'Rất tốt! Hãy thực hành.\n(とても良いです！練習しましょう。)'},
                ]
            else:  # advanced
                messages = [
                    {'side': 'system', 'text': f'＜{phrase.id}＞{phrase.vietnamese_text}\n「{phrase.japanese_translation}」を学ぼう'},
                    {'side': 'left', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'right', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'left', 'text': 'Bạn có thể sử dụng câu này như thế nào?\n(この表現をどう使えますか？)'},
                    {'side': 'right', 'text': 'Tôi nghĩ có thể dùng trong cuộc họp.\n(会議で使えると思います。)'},
                    {'side': 'left', 'text': 'Đúng rồi! Hãy thực hành.\n(その通りです！練習しましょう。)'},
                ]
        else:  # other categories
            messages = [
                {'side': 'system', 'text': f'＜{phrase.id}＞{phrase.vietnamese_text}\n「{phrase.japanese_translation}」を学ぼう'},
                {'side': 'left', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                {'side': 'right', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                {'side': 'left', 'text': 'Lặp lại theo tôi.\n(私が読んだ後に繰り返してください)'},
                {'side': 'left', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                {'side': 'right', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                {'side': 'system', 'text': '＜練習＞'},
                {'side': 'left', 'text': f'{phrase.japanese_translation}！\n({phrase.vietnamese_text}!)'},
                {'side': 'right', 'text': f'{phrase.vietnamese_text}！\n({phrase.japanese_translation}!)'},
            ]
    else:
        # Fallback conversation if no phrase
        messages = [
            {'side': 'system', 'text': '＜学習セッション＞\n「学習セッション」を始めましょう'},
            {'side': 'left', 'text': 'Xin chào! Tôi là giáo viên.\n(こんにちは！私は先生です。)'},
            {'side': 'right', 'text': 'Xin chào! Tôi rất vui được gặp bạn.\n(こんにちは！お会いできて嬉しいです。)'},
            {'side': 'left', 'text': 'Hôm nay chúng ta sẽ học tiếng Việt.\n(今日はベトナム語を学びましょう。)'},
            {'side': 'right', 'text': 'Vâng, tôi rất thích.\n(はい、とても楽しみです。)'},
        ]
    
    context = {
        'partner_id': partner_id,
        'post_id': post_id,
        'phrase_id': phrase.id if phrase else phrase_id,
        'timer_flag': True,  # Enable timer by default
        'poster_gender': poster.gender if poster else None,
        'poster_nationality': poster.nationality if poster else None,
        'poster_city': poster.city if poster else None,
        'poster': poster,
        'post': post,  # Add post to context
        'phrase': phrase,
        'messages': messages,
        'left_icon': 'images/session/teacher.png',
        'left_name': '先生/giáo viên',
        'right_icon': 'images/session/student.png',
        'right_name': '生徒/học sinh',
    }
    
    return render(request, 'session/learning_session.html', context)

@login_required
def start_session_from_dashboard(request):
    """
    Start a new session from dashboard
    This view handles the "Bắt đầu phiên làm việc" button from dashboard
    """
    try:
        # Check if user has any existing posts
        user_posts = LanguageExchangePost.objects.filter(
            japanese_user=request.user
        ) | LanguageExchangePost.objects.filter(
            vietnamese_user=request.user
        )
        
        # If user has posts, redirect to my_posts
        if user_posts.exists():
            return redirect('my_posts')
        
        # If no posts, redirect to create post
        return redirect('create_post')
        
    except Exception as e:
        print(f"DEBUG: Error in start_session_from_dashboard: {e}")
        # Fallback to create post
        return redirect('create_post')

@login_required
def start_working_session(request, post_id):
    """
    Start working session for language exchange
    This view handles the "Bắt đầu phiên làm việc" button from my_posts.html
    """
    post = get_object_or_404(LanguageExchangePost, id=post_id)
    
    # Check if user has access to this post
    if request.user not in [post.japanese_user, post.vietnamese_user]:
        messages.error(request, 'Bạn không có quyền truy cập vào phiên học này.')
        return redirect('/auth/dashboard/')
    
    # Check if post is matched
    if post.status != 'matched':
        messages.error(request, 'Chỉ có thể bắt đầu phiên học khi đã được kết nối.')
        return redirect('/auth/dashboard/')
    
    # Get the appropriate phrase based on user nationality and what they want to learn
    phrase = None
    
    # Debug logging
    print(f"DEBUG WORKING: User nationality: {request.user.nationality}")
    print(f"DEBUG WORKING: User ID: {request.user.id}")
    print(f"DEBUG WORKING: User username: {request.user.username}")
    print(f"DEBUG WORKING: Post ID: {post_id}")
    print(f"DEBUG WORKING: Post phrase: {post.phrase}")
    print(f"DEBUG WORKING: Post accepted_phrase: {post.accepted_phrase}")
    print(f"DEBUG WORKING: Post japanese_learning_phrases count: {post.japanese_learning_phrases.count()}")
    print(f"DEBUG WORKING: Post vietnamese_learning_phrases count: {post.vietnamese_learning_phrases.count()}")
    
    # Check if user is authenticated
    if not request.user.is_authenticated:
        print(f"DEBUG: User is not authenticated!")
        return redirect('/auth/login/')
    
    # Check if nationality is set
    if not hasattr(request.user, 'nationality') or not request.user.nationality:
        print(f"DEBUG: User nationality is not set!")
        # Try to get from profile
        try:
            from user_profile.models import CustomUser
            user_profile = CustomUser.objects.get(id=request.user.id)
            print(f"DEBUG: User profile nationality: {user_profile.nationality}")
            request.user.nationality = user_profile.nationality
        except Exception as e:
            print(f"DEBUG: Error getting user profile: {e}")
            request.user.nationality = 'unknown'
    
    if request.user.nationality == 'japanese':
        # Japanese user wants to learn Vietnamese phrases
        print(f"DEBUG WORKING: Japanese user - checking japanese_learning_phrases")
        if post.japanese_learning_phrases.exists():
            # Use the first phrase from japanese_learning_phrases, or the accepted_phrase if available
            phrase = post.accepted_phrase if post.accepted_phrase else post.japanese_learning_phrases.first()
            print(f"DEBUG WORKING: Japanese user - selected phrase: {phrase}")
        else:
            # Fallback to main phrase
            phrase = post.phrase
            print(f"DEBUG WORKING: Japanese user - fallback to main phrase: {phrase}")
    elif request.user.nationality == 'vietnamese':
        # Vietnamese user wants to learn Japanese phrases
        print(f"DEBUG WORKING: Vietnamese user - checking vietnamese_learning_phrases")
        if post.vietnamese_learning_phrases.exists():
            # Use the first phrase from vietnamese_learning_phrases, or the accepted_phrase if available
            phrase = post.accepted_phrase if post.accepted_phrase else post.vietnamese_learning_phrases.first()
            print(f"DEBUG WORKING: Vietnamese user - selected phrase: {phrase}")
        else:
            # Fallback to main phrase
            phrase = post.phrase
            print(f"DEBUG WORKING: Vietnamese user - fallback to main phrase: {phrase}")
    else:
        # Fallback to main phrase for other nationalities
        phrase = post.phrase
        print(f"DEBUG WORKING: Other nationality - using main phrase: {phrase}")
    
    print(f"DEBUG WORKING: Final selected phrase: {phrase}")
    
    # If still no phrase, create a default one
    if not phrase:
        print(f"DEBUG WORKING: No phrase found, creating default conversation")
        # Create a default phrase object for fallback
        class DefaultPhrase:
            def __init__(self):
                self.id = 1
                self.vietnamese_text = "Xin chào"
                self.japanese_translation = "こんにちは"
                self.category = "greetings"
                self.difficulty = "beginner"
        
        phrase = DefaultPhrase()
    
    # Determine conversation content based on phrase category and difficulty
    if phrase:
        category = phrase.category
        difficulty = phrase.difficulty
        
        # Generate conversation based on category and difficulty
        if category == 'greetings':
            if difficulty == 'beginner':
                messages = [
                    {'side': 'system', 'text': f'＜{phrase.id}＞{phrase.vietnamese_text}\n「{phrase.japanese_translation}」を学ぼう'},
                    {'side': 'left', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'right', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'left', 'text': 'Lặp lại theo tôi.\n(私が読んだ後に繰り返してください)'},
                    {'side': 'left', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'right', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'system', 'text': '＜練習＞　Lặp lại và đối thoại ngắn'},
                    {'side': 'left', 'text': f'{phrase.japanese_translation}。私は{post.japanese_user.full_name or post.japanese_user.username}です。\n({phrase.vietnamese_text}. Tôi là {post.japanese_user.full_name or post.japanese_user.username}.)'},
                    {'side': 'right', 'text': f'{phrase.japanese_translation}。私は{post.vietnamese_user.full_name or post.vietnamese_user.username}です。\n({phrase.vietnamese_text}. Tôi là {post.vietnamese_user.full_name or post.vietnamese_user.username}.)'},
                ]
            elif difficulty == 'intermediate':
                messages = [
                    {'side': 'system', 'text': f'＜{phrase.id}＞{phrase.vietnamese_text}\n「{phrase.japanese_translation}」を学ぼう'},
                    {'side': 'left', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'right', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'left', 'text': 'Bạn có thể lặp lại không?\n(繰り返せますか？)'},
                    {'side': 'right', 'text': f'Vâng, {phrase.vietnamese_text}\n(はい、{phrase.japanese_translation})'},
                    {'side': 'left', 'text': 'Rất tốt! Bây giờ hãy thực hành.\n(とても良いです！今度は練習しましょう。)'},
                    {'side': 'system', 'text': '＜会話練習＞'},
                    {'side': 'left', 'text': f'{phrase.japanese_translation}！私は{post.japanese_user.full_name or post.japanese_user.username}です。\n({phrase.vietnamese_text}! Tôi là {post.japanese_user.full_name or post.japanese_user.username}.)'},
                    {'side': 'right', 'text': f'{phrase.japanese_translation}！Tôi rất vui được gặp bạn.\n({phrase.vietnamese_text}! Rất vui được gặp bạn.)'},
                ]
            else:  # advanced
                messages = [
                    {'side': 'system', 'text': f'＜{phrase.id}＞{phrase.vietnamese_text}\n「{phrase.japanese_translation}」を学ぼう'},
                    {'side': 'left', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'right', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'left', 'text': 'Bạn có thể sử dụng câu này trong tình huống nào?\n(この表現はどんな場面で使えますか？)'},
                    {'side': 'right', 'text': 'Tôi nghĩ có thể dùng khi gặp người mới.\n(新しい人に会った時に使えると思います。)'},
                    {'side': 'left', 'text': 'Đúng rồi! Hãy thực hành với tôi.\n(その通りです！一緒に練習しましょう。)'},
                    {'side': 'system', 'text': '＜応用練習＞'},
                    {'side': 'left', 'text': f'{phrase.japanese_translation}！私は{post.japanese_user.full_name or post.japanese_user.username}です。\n({phrase.vietnamese_text}! Tôi là {post.japanese_user.full_name or post.japanese_user.username}.)'},
                    {'side': 'right', 'text': f'{phrase.japanese_translation}！Tôi rất vui được gặp bạn. Bạn có khỏe không?\n({phrase.vietnamese_text}! Rất vui được gặp bạn. Bạn có khỏe không?)'},
                ]
        elif category == 'food':
            if difficulty == 'beginner':
                messages = [
                    {'side': 'system', 'text': f'＜{phrase.id}＞{phrase.vietnamese_text}\n「{phrase.japanese_translation}」を学ぼう'},
                    {'side': 'left', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'right', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'left', 'text': 'Đây là câu nói về ẩm thực.\n(これは料理についての表現です。)'},
                    {'side': 'right', 'text': 'Tôi hiểu rồi. Có thể lặp lại không?\n(分かりました。繰り返せますか？)'},
                    {'side': 'left', 'text': f'Vâng, {phrase.vietnamese_text}\n(はい、{phrase.japanese_translation})'},
                    {'side': 'right', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'system', 'text': '＜練習＞　Thực hành về ẩm thực'},
                    {'side': 'left', 'text': f'{phrase.japanese_translation}！Tôi thích món này.\n({phrase.vietnamese_text}! Tôi thích món này.)'},
                    {'side': 'right', 'text': f'{phrase.vietnamese_text}！Tôi cũng thích.\n({phrase.japanese_translation}! Tôi cũng thích.)'},
                ]
            elif difficulty == 'intermediate':
                messages = [
                    {'side': 'system', 'text': f'＜{phrase.id}＞{phrase.vietnamese_text}\n「{phrase.japanese_translation}」を学ぼう'},
                    {'side': 'left', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'right', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'left', 'text': 'Bạn có thể giải thích ý nghĩa không?\n(意味を説明できますか？)'},
                    {'side': 'right', 'text': 'Tôi nghĩ có nghĩa là...\n(意味は...だと思います。)'},
                    {'side': 'left', 'text': 'Rất tốt! Hãy thực hành.\n(とても良いです！練習しましょう。)'},
                    {'side': 'system', 'text': '＜会話練習＞'},
                    {'side': 'left', 'text': f'{phrase.japanese_translation}！Bạn có muốn ăn món này không?\n({phrase.vietnamese_text}! Bạn có muốn ăn món này không?)'},
                    {'side': 'right', 'text': f'{phrase.vietnamese_text}！Vâng, tôi rất muốn.\n({phrase.japanese_translation}! Vâng, tôi rất muốn.)'},
                ]
            else:  # advanced
                messages = [
                    {'side': 'system', 'text': f'＜{phrase.id}＞{phrase.vietnamese_text}\n「{phrase.japanese_translation}」を学ぼう'},
                    {'side': 'left', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'right', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'left', 'text': 'Bạn có thể sử dụng câu này như thế nào?\n(この表現をどう使えますか？)'},
                    {'side': 'right', 'text': 'Tôi nghĩ có thể dùng khi gọi món.\n(料理を注文する時に使えると思います。)'},
                    {'side': 'left', 'text': 'Đúng rồi! Hãy thực hành.\n(その通りです！練習しましょう。)'},
                    {'side': 'system', 'text': '＜応用練習＞'},
                    {'side': 'left', 'text': f'{phrase.japanese_translation}！Tôi muốn gọi món này.\n({phrase.vietnamese_text}! Tôi muốn gọi món này.)'},
                    {'side': 'right', 'text': f'{phrase.vietnamese_text}！Tôi cũng muốn thử.\n({phrase.japanese_translation}! Tôi cũng muốn thử.)'},
                ]
        elif category == 'business':
            if difficulty == 'beginner':
                messages = [
                    {'side': 'system', 'text': f'＜{phrase.id}＞{phrase.vietnamese_text}\n「{phrase.japanese_translation}」を学ぼう'},
                    {'side': 'left', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'right', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'left', 'text': 'Đây là câu nói trong môi trường công việc.\n(これは仕事の場面で使う表現です。)'},
                    {'side': 'right', 'text': 'Tôi hiểu rồi. Có thể lặp lại không?\n(分かりました。繰り返せますか？)'},
                    {'side': 'left', 'text': f'Vâng, {phrase.vietnamese_text}\n(はい、{phrase.japanese_translation})'},
                    {'side': 'right', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                ]
            elif difficulty == 'intermediate':
                messages = [
                    {'side': 'system', 'text': f'＜{phrase.id}＞{phrase.vietnamese_text}\n「{phrase.japanese_translation}」を学ぼう'},
                    {'side': 'left', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'right', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'left', 'text': 'Bạn có thể giải thích ý nghĩa không?\n(意味を説明できますか？)'},
                    {'side': 'right', 'text': 'Tôi nghĩ có nghĩa là...\n(意味は...だと思います。)'},
                    {'side': 'left', 'text': 'Rất tốt! Hãy thực hành.\n(とても良いです！練習しましょう。)'},
                ]
            else:  # advanced
                messages = [
                    {'side': 'system', 'text': f'＜{phrase.id}＞{phrase.vietnamese_text}\n「{phrase.japanese_translation}」を学ぼう'},
                    {'side': 'left', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'right', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                    {'side': 'left', 'text': 'Bạn có thể sử dụng câu này như thế nào?\n(この表現をどう使えますか？)'},
                    {'side': 'right', 'text': 'Tôi nghĩ có thể dùng trong cuộc họp.\n(会議で使えると思います。)'},
                    {'side': 'left', 'text': 'Đúng rồi! Hãy thực hành.\n(その通りです！練習しましょう。)'},
                ]
        else:  # other categories
            messages = [
                {'side': 'system', 'text': f'＜{phrase.id}＞{phrase.vietnamese_text}\n「{phrase.japanese_translation}」を学ぼう'},
                {'side': 'left', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                {'side': 'right', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                {'side': 'left', 'text': 'Lặp lại theo tôi.\n(私が読んだ後に繰り返してください)'},
                {'side': 'left', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                {'side': 'right', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
                {'side': 'system', 'text': '＜練習＞'},
                {'side': 'left', 'text': f'{phrase.japanese_translation}！\n({phrase.vietnamese_text}!)'},
                {'side': 'right', 'text': f'{phrase.vietnamese_text}！\n({phrase.japanese_translation}!)'},
            ]
    else:
        # Fallback conversation if no phrase
        messages = [
            {'side': 'system', 'text': '＜学習セッション＞\n「学習セッション」を始めましょう'},
            {'side': 'left', 'text': 'Xin chào! Tôi là giáo viên.\n(こんにちは！私は先生です。)'},
            {'side': 'right', 'text': 'Xin chào! Tôi rất vui được gặp bạn.\n(こんにちは！お会いできて嬉しいです。)'},
            {'side': 'left', 'text': 'Hôm nay chúng ta sẽ học tiếng Việt.\n(今日はベトナム語を学びましょう。)'},
            {'side': 'right', 'text': 'Vâng, tôi rất thích.\n(はい、とても楽しみです。)'},
        ]
    
    # Determine partner info
    if request.user == post.japanese_user:
        partner_id = post.vietnamese_user.id
        poster = post.vietnamese_user
    else:
        partner_id = post.japanese_user.id
        poster = post.japanese_user
    
    context = {
        'partner_id': partner_id,
        'post_id': post_id,
        'phrase_id': phrase.id if phrase else 1,
        'timer_flag': True,  # Enable timer by default
        'poster_gender': poster.gender if poster else None,
        'poster_nationality': poster.nationality if poster else None,
        'poster_city': poster.city if poster else None,
        'poster': poster,
        'phrase': phrase,
        'messages': messages,
        'left_icon': 'images/session/teacher.png',
        'left_name': '先生/giáo viên',
        'right_icon': 'images/session/student.png',
        'right_name': '生徒/học sinh',
        'post': post,
    }
    
    return render(request, 'session/learning_session.html', context)