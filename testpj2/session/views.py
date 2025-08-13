from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from user_profile.models import CustomUser
from event_creation.models import LanguageExchangePost
from django.shortcuts import render

def study(request, partner_id, post_id, phrase_id):
    timer_flag = request.GET.get('timer') == '1'
    template_name = f'session/study_{phrase_id}.html'
    context = {
        'partner_id': partner_id,
        'post_id': post_id,
        'phrase_id': phrase_id,
        'timer_flag': timer_flag,
    }
    return render(request, template_name, context)

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

    # 評価後のリダイレクト先（例：ダッシュボード）
    return redirect('/auth/dashboard/')