import os
import re
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from user_profile.models import CustomUser
from event_creation.models import LanguageExchangePost
from django.shortcuts import render

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
    template_name = f'session/study_{phrase_id}.html'
    
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
        'timer_flag': timer_flag,
        'poster_gender': poster.gender if poster else None,
        'poster_nationality': poster.nationality if poster else None,
        'poster_city': poster.city if poster else None,
        'poster': poster,
    }
    return render(request, template_name, context)

def evaluate(request, partner_id, post_id, phrase_id):
    score_range = range(1, 11)  # 1〜10
    
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

    # ポイント加算
    partner.point += score
    partner.save()

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
    if phrase_id == 1:
        messages = [
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
    elif phrase_id == 2:
        # Chủ đề: Chào buổi sáng
        messages = [
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
    elif phrase_id == 3:
        # Chủ đề: Chào buổi trưa
        messages = [
            {'side': 'system', 'text': '＜３＞Chào buổi trưa\n「こんにちは」を学ぼう'},
            {'side': 'left', 'text': 'Chào buổi trưa.\n(こんにちは。)'},
            {'side': 'right', 'text': 'Chào buổi trưa.\n(こんにちは。)'},
            {'side': 'left', 'text': 'Bạn đã ăn trưa chưa？\n(もうお昼ご飯を食べましたか？)'},
            {'side': 'right', 'text': 'Chưa, mình định đi ăn bây giờ.\n(まだです。これから食べに行く予定です。)'},
            {'side': 'left', 'text': 'Chúc bữa trưa vui vẻ.\n(良いお昼を。)'},
            {'side': 'right', 'text': 'Cảm ơn bạn.\n(ありがとうございます。)'},
        ]
    elif phrase_id == 4:
        # Chủ đề: Chào buổi tối
        messages = [
            {'side': 'system', 'text': '＜４＞Chào buổi tối\n「こんばんは」を学ぼう'},
            {'side': 'left', 'text': 'Chào buổi tối.\n(こんばんは。)'},
            {'side': 'right', 'text': 'Chào buổi tối.\n(こんばんは。)'},
            {'side': 'left', 'text': 'Bạn đã ăn tối chưa？\n(もう夕食を食べましたか？)'},
            {'side': 'right', 'text': 'Rồi, mình đã ăn rồi.\n(はい、もう食べました。)'},
            {'side': 'left', 'text': 'Chúc ngủ ngon sau nhé.\n(おやすみなさい。)'},
            {'side': 'right', 'text': 'Ngủ ngon nhé.\n(おやすみなさい。)'},
        ]
    elif phrase_id == 5:
        # Chủ đề: Bạn khỏe không?
        messages = [
            {'side': 'system', 'text': '＜５＞Bạn khỏe không\n「お元気ですか？」を学ぼう'},
            {'side': 'left', 'text': 'Bạn khỏe không?\n(お元気ですか？)'},
            {'side': 'right', 'text': 'Bạn khỏe không?\n(お元気ですか？)'},
            {'side': 'left', 'text': 'Hôm nay bạn có khỏe không?\n(今日はお元気ですか？)'},
            {'side': 'right', 'text': 'Tôi hơi mệt nhưng ổn.\n(少し疲れていますが、大丈夫です。)'},
            {'side': 'left', 'text': 'Bạn có cần nghỉ không?\n(休んだ方がいいですか？)'},
            {'side': 'right', 'text': 'Không, cảm ơn. Tôi ổn.\n(いいえ、大丈夫です。ありがとう。)'},
        ]
    elif phrase_id == 6:
        # Chủ đề: Tôi khỏe, cảm ơn
        messages = [
            {'side': 'system', 'text': '＜６＞Tôi khỏe, cảm ơn\n「元気です、ありがとう」を学ぼう'},
            {'side': 'left', 'text': 'Tôi khỏe, cảm ơn.\n(元気です、ありがとう。)'},
            {'side': 'right', 'text': 'Tôi khỏe, cảm ơn.\n(元気です、ありがとう。)'},
            {'side': 'left', 'text': 'Rất vui khi nghe vậy.\n(それは良かったです。)'},
            {'side': 'right', 'text': 'Cảm ơn bạn.\n(ありがとうございます。)'},
            {'side': 'left', 'text': 'Nếu mệt thì hãy nghỉ nhé.\n(疲れたら休んでくださいね。)'},
        ]
    else:
        messages = []

    context = {
        'messages': messages,
        'left_icon': 'images/session/teacher.png',
        'left_name': '先生/giáo viên',
        'right_icon': 'images/session/student.png',
        'right_name': '生徒/học sinh',
    }
    return render(request, 'session/study.html', context)