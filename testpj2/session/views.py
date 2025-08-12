from django.shortcuts import get_object_or_404, render

def study(request, post_id, phrase_id):
    timer_flag = request.GET.get('timer') == '1'
    template_name = f'session/study_{phrase_id}.html'
    context = {
        'post_id': post_id,
        'phrase_id': phrase_id,
        'timer_flag': timer_flag,
    }
    return render(request, template_name, context)
