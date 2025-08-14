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

def study(request, partner_id, post_id, phrase_id=None):
    timer_flag = request.GET.get('timer') == '1'
    
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
    
    # Determine which template to use based on learning phrases
    if phrase_id:
        template_name = f'session/study_{phrase_id}.html'
    else:
        # Use default template if no specific phrase_id
        template_name = 'session/study.html'
    
    context = {
        'partner_id': partner_id,
        'post_id': post_id,
        'phrase_id': phrase_id,
        'timer_flag': timer_flag,
        'poster_gender': poster.gender if poster else None,
        'poster_nationality': poster.nationality if poster else None,
        'poster_city': poster.city if poster else None,
        'poster': poster,
        'post': post,  # Add post to context for template access
    }
    return render(request, template_name, context)

def evaluate(request, partner_id, post_id, phrase_id=None):
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
        'post': post,  # Add post to context for template access
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
            {'side': 'left', 'text': 'Bạn là giáo viên.\n(あなたは先生です。)'},
            {'side': 'right', 'text': 'Bạn là giáo viên.\n(あなたは先生です。)'},
            {'side': 'left', 'text': 'Bạn là học sinh.\n(あなたは学生です。)'},
            {'side': 'right', 'text': 'Bạn là học sinh.\n(あなたは学生です。)'},
            {'side': 'left', 'text': 'Bạn là người Việt Nam.\n(あなたはベトナム人です。)'},
            {'side': 'right', 'text': 'Bạn là người Việt Nam.\n(あなたはベトナム人です。)'},
            {'side': 'left', 'text': 'Bạn là người Nhật.\n(あなたは日本人です。)'},
            {'side': 'right', 'text': 'Bạn là người Nhật.\n(あなたは日本人です。)'},
        ]
    elif phrase_id == 2:
        messages = [
            {'side': 'system', 'text': '＜2＞Chào buổi sáng 「おはよう」を学ぼう'},
            {'side': 'left', 'text': 'Chào buổi sáng. (おはようございます。)'},
            {'side': 'right', 'text': 'Chào buổi sáng. (おはようございます。)'},
            {'side': 'left', 'text': 'Chào nhé! (thân mật) (おはよう。)'},
            {'side': 'right', 'text': 'Chào nhé! (thân mật) (おはよう。)'},
            {'side': 'left', 'text': 'Chào buổi sáng, bạn có khỏe không? (おはよう、お元気ですか？)'},
            {'side': 'right', 'text': 'Chào buổi sáng, bạn có khỏe không? (おはよう、お元気ですか？)'},
            {'side': 'left', 'text': 'Vâng, tôi khỏe. Cảm ơn bạn. (はい、元気です。ありがとう。)'},
            {'side': 'right', 'text': 'Vâng, tôi khỏe. Cảm ơn bạn. (はい、元気です。ありがとう。)'},
        ]
    elif phrase_id == 3:
        messages = [
            {'side': 'system', 'text': '＜3＞Chào buổi trưa 「こんにちは」を学ぼう'},
            {'side': 'left', 'text': 'Chào buổi trưa. (こんにちは。)'},
            {'side': 'right', 'text': 'Chào buổi trưa. (こんにちは。)'},
            {'side': 'left', 'text': 'Chào bạn! (thân mật) (こんにちは！)'},
            {'side': 'right', 'text': 'Chào bạn! (thân mật) (こんにちは！)'},
            {'side': 'left', 'text': 'Bạn đã ăn trưa chưa? (お昼ご飯は食べましたか？)'},
            {'side': 'right', 'text': 'Bạn đã ăn trưa chưa? (お昼ご飯は食べましたか？)'},
            {'side': 'left', 'text': 'Rồi, tôi đã ăn rồi. (はい、食べました。)'},
            {'side': 'right', 'text': 'Rồi, tôi đã ăn rồi. (はい、食べました。)'},
        ]
    elif phrase_id == 4:
        messages = [
            {'side': 'system', 'text': '＜4＞Chào buổi tối 「こんばんは」を学ぼう'},
            {'side': 'left', 'text': 'Chào buổi tối. (こんばんは。)'},
            {'side': 'right', 'text': 'Chào buổi tối. (こんばんは。)'},
            {'side': 'left', 'text': 'Chào bạn! (thân mật) (こんばんは！)'},
            {'side': 'right', 'text': 'Chào bạn! (thân mật) (こんばんは！)'},
            {'side': 'left', 'text': 'Bạn có khỏe không? (お元気ですか？)'},
            {'side': 'right', 'text': 'Bạn có khỏe không? (お元気ですか？)'},
            {'side': 'left', 'text': 'Vâng, tôi khỏe. Cảm ơn bạn. (はい、元気です。ありがとう。)'},
            {'side': 'right', 'text': 'Vâng, tôi khỏe. Cảm ơn bạn. (はい、元気です。ありがとう。)'},
        ]
    elif phrase_id == 5:
        messages = [
            {'side': 'system', 'text': '＜5＞Bạn khỏe không\n「お元気ですか？」を学ぼう'},
            {'side': 'left', 'text': 'Bạn khỏe không?\n(お元気ですか？)'},
            {'side': 'right', 'text': 'Bạn khỏe không?\n(お元気ですか？)'},
            {'side': 'left', 'text': 'Hôm nay bạn có khỏe không?\n(今日はお元気ですか？)'},
            {'side': 'right', 'text': 'Tôi hơi mệt nhưng ổn.\n(少し疲れていますが、大丈夫です。)'},
            {'side': 'left', 'text': 'Bạn có cần nghỉ không?\n(休んだ方がいいですか？)'},
            {'side': 'right', 'text': 'Không, cảm ơn. Tôi ổn.\n(いいえ、大丈夫です。ありがとう。)'},
        ]
    elif phrase_id == 6:
        messages = [
            {'side': 'system', 'text': '＜6＞Tôi khỏe, cảm ơn\n「元気です、ありがとう」を学ぼう'},
            {'side': 'left', 'text': 'Tôi khỏe, cảm ơn.\n(元気です、ありがとう。)'},
            {'side': 'right', 'text': 'Tôi khỏe, cảm ơn.\n(元気です、ありがとう。)'},
            {'side': 'left', 'text': 'Rất vui khi nghe vậy.\n(それは良かったです。)'},
            {'side': 'right', 'text': 'Cảm ơn bạn.\n(ありがとうございます。)'},
            {'side': 'left', 'text': 'Nếu mệt thì hãy nghỉ nhé.\n(疲れたら休んでくださいね。)'},
        ]
    elif phrase_id == 7:
        messages = [
            {'side': 'system', 'text': '＜7＞Chào buổi sáng 「おはよう」を学ぼう'},
            {'side': 'left', 'text': 'Chào buổi sáng. (おはようございます。)'},
            {'side': 'right', 'text': 'Chào buổi sáng. (おはようございます。)'},
            {'side': 'left', 'text': 'Chào nhé! (thân mật) (おはよう。)'},
            {'side': 'right', 'text': 'Chào nhé! (thân mật) (おはよう。)'},
            {'side': 'left', 'text': 'Chào buổi sáng, bạn có khỏe không? (おはよう、お元気ですか？)'},
            {'side': 'right', 'text': 'Chào buổi sáng, bạn có khỏe không? (おはよう、お元気ですか？)'},
            {'side': 'left', 'text': 'Vâng, tôi khỏe. Cảm ơn bạn. (はい、元気です。ありがとう。)'},
            {'side': 'right', 'text': 'Vâng, tôi khỏe. Cảm ơn bạn. (はい、元気です。ありがとう。)'},
        ]
    elif phrase_id == 8:
        messages = [
            {'side': 'system', 'text': '＜8＞Chào buổi trưa 「こんにちは」を学ぼう'},
            {'side': 'left', 'text': 'Chào buổi trưa. (こんにちは。)'},
            {'side': 'right', 'text': 'Chào buổi trưa. (こんにちは。)'},
            {'side': 'left', 'text': 'Chào bạn! (thân mật) (こんにちは！)'},
            {'side': 'right', 'text': 'Chào bạn! (thân mật) (こんにちは！)'},
            {'side': 'left', 'text': 'Bạn đã ăn trưa chưa? (お昼ご飯は食べましたか？)'},
            {'side': 'right', 'text': 'Bạn đã ăn trưa chưa? (お昼ご飯は食べましたか？)'},
            {'side': 'left', 'text': 'Rồi, tôi đã ăn rồi. (はい、食べました。)'},
            {'side': 'right', 'text': 'Rồi, tôi đã ăn rồi. (はい、食べました。)'},
        ]
    elif phrase_id == 9:
        messages = [
            {'side': 'system', 'text': '＜9＞Chào buổi tối 「こんばんは」を学ぼう'},
            {'side': 'left', 'text': 'Chào buổi tối. (こんばんは。)'},
            {'side': 'right', 'text': 'Chào buổi tối. (こんばんは。)'},
            {'side': 'left', 'text': 'Chào bạn! (thân mật) (こんばんは！)'},
            {'side': 'right', 'text': 'Chào bạn! (thân mật) (こんばんは！)'},
            {'side': 'left', 'text': 'Bạn có khỏe không? (お元気ですか？)'},
            {'side': 'right', 'text': 'Bạn có khỏe không? (お元気ですか？)'},
            {'side': 'left', 'text': 'Vâng, tôi khỏe. Cảm ơn bạn. (はい、元気です。ありがとう。)'},
            {'side': 'right', 'text': 'Vâng, tôi khỏe. Cảm ơn bạn. (はい、元気です。ありがとう。)'},
        ]
    elif phrase_id == 10:
        messages = [
            {'side': 'system', 'text': '＜10＞Bạn khỏe không\n「お元気ですか？」を学ぼう'},
            {'side': 'left', 'text': 'Bạn khỏe không?\n(お元気ですか？)'},
            {'side': 'right', 'text': 'Bạn khỏe không?\n(お元気ですか？)'},
            {'side': 'left', 'text': 'Hôm nay bạn có khỏe không?\n(今日はお元気ですか？)'},
            {'side': 'right', 'text': 'Tôi hơi mệt nhưng ổn.\n(少し疲れていますが、大丈夫です。)'},
            {'side': 'left', 'text': 'Bạn có cần nghỉ không?\n(休んだ方がいいですか？)'},
            {'side': 'right', 'text': 'Không, cảm ơn. Tôi ổn.\n(いいえ、大丈夫です。ありがとう。)'},
        ]
    elif phrase_id == 11:
        messages = [
            {'side': 'system', 'text': '＜11＞Tôi khỏe, cảm ơn\n「元気です、ありがとう」を学ぼう'},
            {'side': 'left', 'text': 'Tôi khỏe, cảm ơn.\n(元気です、ありがとう。)'},
            {'side': 'right', 'text': 'Tôi khỏe, cảm ơn.\n(元気です、ありがとう。)'},
            {'side': 'left', 'text': 'Rất vui khi nghe vậy.\n(それは良かったです。)'},
            {'side': 'right', 'text': 'Cảm ơn bạn.\n(ありがとうございます。)'},
            {'side': 'left', 'text': 'Nếu mệt thì hãy nghỉ nhé.\n(疲れたら休んでくださいね。)'},
        ]
    elif phrase_id == 12:
        messages = [
            {'side': 'system', 'text': '＜12＞Chào buổi sáng 「おはよう」を学ぼう'},
            {'side': 'left', 'text': 'Chào buổi sáng. (おはようございます。)'},
            {'side': 'right', 'text': 'Chào buổi sáng. (おはようございます。)'},
            {'side': 'left', 'text': 'Chào nhé! (thân mật) (おはよう。)'},
            {'side': 'right', 'text': 'Chào nhé! (thân mật) (おはよう。)'},
            {'side': 'left', 'text': 'Chào buổi sáng, bạn có khỏe không? (おはよう、お元気ですか？)'},
            {'side': 'right', 'text': 'Chào buổi sáng, bạn có khỏe không? (おはよう、お元気ですか？)'},
            {'side': 'left', 'text': 'Vâng, tôi khỏe. Cảm ơn bạn. (はい、元気です。ありがとう。)'},
            {'side': 'right', 'text': 'Vâng, tôi khỏe. Cảm ơn bạn. (はい、元気です。ありがとう。)'},
        ]
    elif phrase_id == 13:
        messages = [
            {'side': 'system', 'text': '＜13＞Chào buổi trưa 「こんにちは」を学ぼう'},
            {'side': 'left', 'text': 'Chào buổi trưa. (こんにちは。)'},
            {'side': 'right', 'text': 'Chào buổi trưa. (こんにちは。)'},
            {'side': 'left', 'text': 'Chào bạn! (thân mật) (こんにちは！)'},
            {'side': 'right', 'text': 'Chào bạn! (thân mật) (こんにちは！)'},
            {'side': 'left', 'text': 'Bạn đã ăn trưa chưa? (お昼ご飯は食べましたか？)'},
            {'side': 'right', 'text': 'Bạn đã ăn trưa chưa? (お昼ご飯は食べましたか？)'},
            {'side': 'left', 'text': 'Rồi, tôi đã ăn rồi. (はい、食べました。)'},
            {'side': 'right', 'text': 'Rồi, tôi đã ăn rồi. (はい、食べました。)'},
        ]
    elif phrase_id == 14:
        messages = [
            {'side': 'system', 'text': '＜14＞Chào buổi tối 「こんばんは」を学ぼう'},
            {'side': 'left', 'text': 'Chào buổi tối. (こんばんは。)'},
            {'side': 'right', 'text': 'Chào buổi tối. (こんばんは。)'},
            {'side': 'left', 'text': 'Chào bạn! (thân mật) (こんばんは！)'},
            {'side': 'right', 'text': 'Chào bạn! (thân mật) (こんばんは！)'},
            {'side': 'left', 'text': 'Bạn có khỏe không? (お元気ですか？)'},
            {'side': 'right', 'text': 'Bạn có khỏe không? (お元気ですか？)'},
            {'side': 'left', 'text': 'Vâng, tôi khỏe. Cảm ơn bạn. (はい、元気です。ありがとう。)'},
            {'side': 'right', 'text': 'Vâng, tôi khỏe. Cảm ơn bạn. (はい、元気です。ありがとう。)'},
        ]
    elif phrase_id == 15:
        messages = [
            {'side': 'system', 'text': '＜15＞Bạn khỏe không\n「お元気ですか？」を学ぼう'},
            {'side': 'left', 'text': 'Bạn khỏe không?\n(お元気ですか？)'},
            {'side': 'right', 'text': 'Bạn khỏe không?\n(お元気ですか？)'},
            {'side': 'left', 'text': 'Hôm nay bạn có khỏe không?\n(今日はお元気ですか？)'},
            {'side': 'right', 'text': 'Tôi hơi mệt nhưng ổn.\n(少し疲れていますが、大丈夫です。)'},
            {'side': 'left', 'text': 'Bạn có cần nghỉ không?\n(休んだ方がいいですか？)'},
            {'side': 'right', 'text': 'Không, cảm ơn. Tôi ổn.\n(いいえ、大丈夫です。ありがとう。)'},
        ]
    elif phrase_id == 16:
        messages = [
            {'side': 'system', 'text': '＜16＞Tôi khỏe, cảm ơn\n「元気です、ありがとう」を学ぼう'},
            {'side': 'left', 'text': 'Tôi khỏe, cảm ơn.\n(元気です、ありがとう。)'},
            {'side': 'right', 'text': 'Tôi khỏe, cảm ơn.\n(元気です、ありがとう。)'},
            {'side': 'left', 'text': 'Rất vui khi nghe vậy.\n(それは良かったです。)'},
            {'side': 'right', 'text': 'Cảm ơn bạn.\n(ありがとうございます。)'},
            {'side': 'left', 'text': 'Nếu mệt thì hãy nghỉ nhé.\n(疲れたら休んでくださいね。)'},
        ]
    elif phrase_id == 17:
        messages = [
            {'side': 'system', 'text': '＜17＞Chào buổi sáng 「おはよう」を学ぼう'},
            {'side': 'left', 'text': 'Chào buổi sáng. (おはようございます。)'},
            {'side': 'right', 'text': 'Chào buổi sáng. (おはようございます。)'},
            {'side': 'left', 'text': 'Chào nhé! (thân mật) (おはよう。)'},
            {'side': 'right', 'text': 'Chào nhé! (thân mật) (おはよう。)'},
            {'side': 'left', 'text': 'Chào buổi sáng, bạn có khỏe không? (おはよう、お元気ですか？)'},
            {'side': 'right', 'text': 'Chào buổi sáng, bạn có khỏe không? (おはよう、お元気ですか？)'},
            {'side': 'left', 'text': 'Vâng, tôi khỏe. Cảm ơn bạn. (はい、元気です。ありがとう。)'},
            {'side': 'right', 'text': 'Vâng, tôi khỏe. Cảm ơn bạn. (はい、元気です。ありがとう。)'},
        ]
    elif phrase_id == 18:
        messages = [
            {'side': 'system', 'text': '＜18＞Chào buổi trưa 「こんにちは」を学ぼう'},
            {'side': 'left', 'text': 'Chào buổi trưa. (こんにちは。)'},
            {'side': 'right', 'text': 'Chào buổi trưa. (こんにちは。)'},
            {'side': 'left', 'text': 'Chào bạn! (thân mật) (こんにちは！)'},
            {'side': 'right', 'text': 'Chào bạn! (thân mật) (こんにちは！)'},
            {'side': 'left', 'text': 'Bạn đã ăn trưa chưa? (お昼ご飯は食べましたか？)'},
            {'side': 'right', 'text': 'Bạn đã ăn trưa chưa? (お昼ご飯は食べましたか？)'},
            {'side': 'left', 'text': 'Rồi, tôi đã ăn rồi. (はい、食べました。)'},
            {'side': 'right', 'text': 'Rồi, tôi đã ăn rồi. (はい、食べました。)'},
        ]
    elif phrase_id == 19:
        messages = [
            {'side': 'system', 'text': '＜19＞Chào buổi tối 「こんばんは」を学ぼう'},
            {'side': 'left', 'text': 'Chào buổi tối. (こんばんは。)'},
            {'side': 'right', 'text': 'Chào buổi tối. (こんばんは。)'},
            {'side': 'left', 'text': 'Chào bạn! (thân mật) (こんばんは！)'},
            {'side': 'right', 'text': 'Chào bạn! (thân mật) (こんばんは！)'},
            {'side': 'left', 'text': 'Bạn có khỏe không? (お元気ですか？)'},
            {'side': 'right', 'text': 'Bạn có khỏe không? (お元気ですか？)'},
            {'side': 'left', 'text': 'Vâng, tôi khỏe. Cảm ơn bạn. (はい、元気です。ありがとう。)'},
            {'side': 'right', 'text': 'Vâng, tôi khỏe. Cảm ơn bạn. (はい、元気です。ありがとう。)'},
        ]
    elif phrase_id == 20:
        messages = [
            {'side': 'system', 'text': '＜20＞Bạn khỏe không\n「お元気ですか？」を学ぼう'},
            {'side': 'left', 'text': 'Bạn khỏe không?\n(お元気ですか？)'},
            {'side': 'right', 'text': 'Bạn khỏe không?\n(お元気ですか？)'},
            {'side': 'left', 'text': 'Hôm nay bạn có khỏe không?\n(今日はお元気ですか？)'},
            {'side': 'right', 'text': 'Tôi hơi mệt nhưng ổn.\n(少し疲れていますが、大丈夫です。)'},
            {'side': 'left', 'text': 'Bạn có cần nghỉ không?\n(休んだ方がいいですか？)'},
            {'side': 'right', 'text': 'Không, cảm ơn. Tôi ổn.\n(いいえ、大丈夫です。ありがとう。)'},
        ]
    else:
        # For any other phrase_id, create a generic dialogue format
        messages = [
            {'side': 'system', 'text': f'＜{phrase_id}＞Bài học tiếng Việt 「ベトナム語レッスン」を学ぼう'},
            {'side': 'left', 'text': 'Xin chào! (こんにちは！)'},
            {'side': 'right', 'text': 'Xin chào! (こんにちは！)'},
            {'side': 'left', 'text': 'Hôm nay chúng ta sẽ học tiếng Việt. (今日はベトナム語を学びましょう。)'},
            {'side': 'right', 'text': 'Vâng, tôi rất thích. (はい、とても楽しみです。)'},
            {'side': 'left', 'text': 'Hãy lặp lại theo tôi. (私の後に繰り返してください。)'},
            {'side': 'right', 'text': 'Vâng, tôi sẽ lặp lại. (はい、繰り返します。)'},
            {'side': 'left', 'text': 'Rất tốt! (とても良いです！)'},
            {'side': 'right', 'text': 'Cảm ơn bạn! (ありがとうございます！)'},
        ]

    context = {
        'messages': messages,
        'left_icon': 'images/session/teacher.png',
        'left_name': '先生/giáo viên',
        'right_icon': 'images/session/student.png',
        'right_name': '生徒/học sinh',
    }
    return render(request, 'session/study.html', context)


def text_session(request, post_id):
    """
    Simple two-step text session flow:
    step=1: show the original learning phrases from the post creator
    step=2: show the learning phrases from the person who accepted the post
    """
    step_param = request.GET.get('step', '1')
    try:
        step = int(step_param)
    except ValueError:
        step = 1

    post = get_object_or_404(LanguageExchangePost, id=post_id)

    # Determine content based on learning phrases and who created/accepted the post
    if step == 1:
        # Step 1: Show what the original post creator wanted to learn
        if post.vietnamese_user and post.japanese_user is None:
            # Vietnamese user created the post, show what they want to learn
            content_title = 'Các câu nói tiếng Nhật muốn học (Vietnamese Learning)'
            if post.vietnamese_learning_phrases.exists():
                phrases = post.vietnamese_learning_phrases.all()
                content_text = '\n'.join([f"• {phrase.vietnamese_text} ({phrase.get_category_display()})" for phrase in phrases])
            else:
                content_text = 'Không có câu nói nào được chọn'
        else:
            # Japanese user created the post, show what they want to learn
            content_title = 'Các câu nói tiếng Việt muốn học (Japanese Learning)'
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
        # Step 2: Show what the person who accepted the post wants to learn
        if post.vietnamese_user and post.japanese_user:
            # Post is matched, show what the Japanese user wants to learn
            content_title = 'Các câu nói tiếng Việt muốn học (Japanese Learning)'
            if post.japanese_learning_phrases.exists():
                phrases = post.japanese_learning_phrases.all()
                content_text = '\n'.join([f"• {phrase.vietnamese_text} ({phrase.get_category_display()})" for phrase in phrases])
            else:
                content_text = 'Không có câu nói nào được chọn'
        else:
            # Post is not matched yet, show default message
            content_title = 'Các câu nói muốn học'
            content_text = 'Bài đăng chưa được chấp nhận'
        
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
def start_working_session(request, post_id):
    """
    Start working session and show appropriate learning content for each user:
    - Poster learns what they chose in their post
    - Accepter learns what they chose when applying
    """
    post = get_object_or_404(LanguageExchangePost, id=post_id)
    
    # Check if user has access to this post
    if request.user not in [post.japanese_user, post.vietnamese_user]:
        messages.error(request, 'Bạn không có quyền truy cập vào phiên học này.')
        return redirect('/auth/dashboard/')
    
    # Check if post is matched
    if post.status != 'matched':
        messages.error(request, 'Bài đăng chưa được kết nối hoàn toàn.')
        return redirect('/auth/dashboard/')
    
    # Determine what content to show based on user role and their chosen phrases
    if request.user == post.japanese_user:
        # Japanese user - check if they are the poster or accepter
        if post.japanese_user == request.user and post.vietnamese_user != request.user:
            # Japanese user is the poster - show what they chose to learn
            if post.japanese_learning_phrases.exists():
                chosen_phrase = post.japanese_learning_phrases.first()
                lesson_title = f"Bài học tiếng Việt: {chosen_phrase.vietnamese_text}"
                lesson_content = f"""
                <h4>Bạn đã chọn học: {chosen_phrase.vietnamese_text}</h4>
                <p><strong>Phát âm:</strong> {chosen_phrase.vietnamese_text}</p>
                <p><strong>Ý nghĩa tiếng Nhật:</strong> {chosen_phrase.japanese_translation}</p>
                <p><strong>Ý nghĩa tiếng Anh:</strong> {chosen_phrase.english_translation}</p>
                
                <h5>Thông tin chi tiết:</h5>
                <ul>
                    <li><strong>Danh mục:</strong> {chosen_phrase.get_category_display()}</li>
                    <li><strong>Độ khó:</strong> {chosen_phrase.get_difficulty_display()}</li>
                    <li><strong>Dịch tiếng Nhật:</strong> {chosen_phrase.japanese_translation}</li>
                    <li><strong>Dịch tiếng Anh:</strong> {chosen_phrase.english_translation}</li>
                </ul>
                
                <h5>Hướng dẫn học tập:</h5>
                <p>Đây là câu nói tiếng Việt mà bạn đã chọn để học. Hãy luyện tập phát âm và hiểu ý nghĩa để có thể sử dụng trong giao tiếp thực tế với partner.</p>
                """
            else:
                lesson_title = "Bài học tiếng Việt"
                lesson_content = """
                <h4>Bạn chưa chọn câu nói cụ thể để học</h4>
                <p>Để có trải nghiệm học tập tốt nhất, hãy chọn các câu nói tiếng Việt mà bạn muốn học.</p>
                """
        else:
            # Japanese user is the accepter - show what they chose when applying
            if post.accepted_phrase:
                chosen_phrase = post.accepted_phrase
                lesson_title = f"Bài học tiếng Việt: {chosen_phrase.vietnamese_text}"
                lesson_content = f"""
                <h4>Bạn đã chọn học: {chosen_phrase.vietnamese_text}</h4>
                <p><strong>Phát âm:</strong> {chosen_phrase.vietnamese_text}</p>
                <p><strong>Ý nghĩa tiếng Nhật:</strong> {chosen_phrase.japanese_translation}</p>
                <p><strong>Ý nghĩa tiếng Anh:</strong> {chosen_phrase.english_translation}</p>
                
                <h5>Thông tin chi tiết:</h5>
                <ul>
                    <li><strong>Danh mục:</strong> {chosen_phrase.get_category_display()}</li>
                    <li><strong>Độ khó:</strong> {chosen_phrase.get_difficulty_display()}</li>
                    <li><strong>Dịch tiếng Nhật:</strong> {chosen_phrase.japanese_translation}</li>
                    <li><strong>Dịch tiếng Anh:</strong> {chosen_phrase.english_translation}</li>
                </ul>
                
                <h5>Hướng dẫn học tập:</h5>
                <p>Đây là câu nói tiếng Việt mà bạn đã chọn khi ứng tuyển. Hãy luyện tập phát âm và hiểu ý nghĩa để có thể sử dụng trong giao tiếp thực tế với partner.</p>
                """
            else:
                lesson_title = "Bài học tiếng Việt"
                lesson_content = """
                <h4>Bạn chưa chọn câu nói cụ thể để học</h4>
                <p>Để có trải nghiệm học tập tốt nhất, hãy chọn các câu nói tiếng Việt mà bạn muốn học.</p>
                """
        lesson_type = "japanese_learning"
        
    elif request.user == post.vietnamese_user:
        # Vietnamese user - check if they are the poster or accepter
        if post.vietnamese_user == request.user and post.japanese_user != request.user:
            # Vietnamese user is the poster - show what they chose to learn
            if post.vietnamese_learning_phrases.exists():
                chosen_phrase = post.vietnamese_learning_phrases.first()
                lesson_title = f"Bài học tiếng Nhật: {chosen_phrase.vietnamese_text}"
                lesson_content = f"""
                <h4>Bạn đã chọn học: {chosen_phrase.vietnamese_text}</h4>
                <p><strong>Phát âm:</strong> {chosen_phrase.vietnamese_text}</p>
                <p><strong>Ý nghĩa tiếng Nhật:</strong> {chosen_phrase.japanese_translation}</p>
                <p><strong>Ý nghĩa tiếng Anh:</strong> {chosen_phrase.english_translation}</p>
                
                <h5>Thông tin chi tiết:</h5>
                <ul>
                    <li><strong>Danh mục:</strong> {chosen_phrase.get_category_display()}</li>
                    <li><strong>Độ khó:</strong> {chosen_phrase.get_difficulty_display()}</li>
                    <li><strong>Dịch tiếng Nhật:</strong> {chosen_phrase.japanese_translation}</li>
                    <li><strong>Dịch tiếng Anh:</strong> {chosen_phrase.english_translation}</li>
                </ul>
                
                <h5>Hướng dẫn học tập:</h5>
                <p>Đây là câu nói tiếng Nhật mà bạn đã chọn để học. Hãy luyện tập phát âm và hiểu ý nghĩa để có thể sử dụng trong giao tiếp thực tế với partner.</p>
                """
            else:
                lesson_title = "Bài học tiếng Nhật"
                lesson_content = """
                <h4>Bạn chưa chọn câu nói cụ thể để học</h4>
                <p>Để có trải nghiệm học tập tốt nhất, hãy chọn các câu nói tiếng Nhật mà bạn muốn học.</p>
                """
        else:
            # Vietnamese user is the accepter - show what they chose when applying
            if post.accepted_phrase:
                chosen_phrase = post.accepted_phrase
                lesson_title = f"Bài học tiếng Nhật: {chosen_phrase.vietnamese_text}"
                lesson_content = f"""
                <h4>Bạn đã chọn học: {chosen_phrase.vietnamese_text}</h4>
                <p><strong>Phát âm:</strong> {chosen_phrase.vietnamese_text}</p>
                <p><strong>Ý nghĩa tiếng Nhật:</strong> {chosen_phrase.japanese_translation}</p>
                <p><strong>Ý nghĩa tiếng Anh:</strong> {chosen_phrase.english_translation}</p>
                
                <h5>Thông tin chi tiết:</h5>
                <ul>
                    <li><strong>Danh mục:</strong> {chosen_phrase.get_category_display()}</li>
                    <li><strong>Độ khó:</strong> {chosen_phrase.get_difficulty_display()}</li>
                    <li><strong>Dịch tiếng Nhật:</strong> {chosen_phrase.japanese_translation}</li>
                    <li><strong>Dịch tiếng Anh:</strong> {chosen_phrase.english_translation}</li>
                </ul>
                
                <h5>Hướng dẫn học tập:</h5>
                <p>Đây là câu nói tiếng Nhật mà bạn đã chọn khi ứng tuyển. Hãy luyện tập phát âm và hiểu ý nghĩa để có thể sử dụng trong giao tiếp thực tế với partner.</p>
                """
            else:
                lesson_title = "Bài học tiếng Nhật"
                lesson_content = """
                <h4>Bạn chưa chọn câu nói cụ thể để học</h4>
                <p>Để có trải nghiệm học tập tốt nhất, hãy chọn các câu nói tiếng Nhật mà bạn muốn học.</p>
                """
        lesson_type = "vietnamese_learning"
        
    else:
        # Fallback case
        lesson_title = "Bài học ngôn ngữ"
        lesson_content = "<p>Không thể xác định nội dung bài học.</p>"
        lesson_type = "unknown"
    
    context = {
        'post': post,
        'lesson_title': lesson_title,
        'lesson_content': lesson_content,
        'lesson_type': lesson_type,
        'partner': post.vietnamese_user if request.user == post.japanese_user else post.japanese_user,
    }
    
    return render(request, 'session/working_session.html', context)