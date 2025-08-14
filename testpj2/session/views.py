import os
import re
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from user_profile.models import CustomUser
from event_creation.models import LanguageExchangePost
from django.shortcuts import render

def study(request, partner_id, post_id, phrase_id):
    timer_flag = request.GET.get('timer') == '1'
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
        messages = [
        ]
    else:
        messages = []

    context = {
        'partner_id': partner_id,
        'post_id': post_id,
        'phrase_id': phrase_id,
        'timer_flag': timer_flag,
        'messages': messages,
        'left_icon': 'images/session/teacher.png',
        'left_name': '先生/giáo viên',
        'right_icon': 'images/session/student.png',
        'right_name': '生徒/học sinh',
    }
    return render(request, 'session/study.html', context)

def evaluate(request, partner_id, post_id, phrase_id):
    score_range = range(1, 11)  # 1〜10
    context = {
        'partner_id': partner_id,
        'post_id': post_id,
        'phrase_id': phrase_id,
        'score_range': score_range,
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
            {'side': 'left', 'text': 'Bạn là giáo viên.\n(あなたは先生です。)'},
            {'side': 'right', 'text': 'Bạn là giáo viên.\n(あなたは先生です。)'},
            {'side': 'left', 'text': 'Bạn là học sinh.\n(あなたは学生です。)'},
            {'side': 'right', 'text': 'Bạn là học sinh.\n(あなたは学生です。)'},
            {'side': 'left', 'text': 'Bạn là người Việt Nam.\n(あなたはベトナム人です。)'},
            {'side': 'right', 'text': 'Bạn là người Việt Nam.\n(あなたはベトナム人です。)'},
            {'side': 'left', 'text': 'Bạn là người Nhật.\n(あなたは日本人です。)'},
            {'side': 'right', 'text': 'Bạn là người Nhật.\n(あなたは日本人です。)'},
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
        messages = [
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