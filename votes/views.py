from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Poll, Choice, Vote
from django.utils import timezone

def is_moderator_or_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

def vote_list(request):
    search_query = request.GET.get('q')
    
    active_polls = Poll.objects.filter(is_active=True, end_date__gte=timezone.now())
    ended_polls = Poll.objects.filter(is_active=False) | Poll.objects.filter(end_date__lt=timezone.now())
    
    if search_query:
        active_polls = active_polls.filter(title__icontains=search_query)
        ended_polls = ended_polls.filter(title__icontains=search_query)
    
    paginator_active = Paginator(active_polls, 10)
    page_active = request.GET.get('page_active')
    active_polls_page = paginator_active.get_page(page_active)
    
    context = {
        'active_polls': active_polls_page,
        'ended_polls': ended_polls,
        'search_query': search_query,
    }
    return render(request, 'votes/vote_list.html', context)

def vote_detail(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    can_vote = poll.can_vote(request.user)
    
    user_vote = None
    if request.user.is_authenticated:
        try:
            user_vote = Vote.objects.get(user=request.user, poll=poll)
        except Vote.DoesNotExist:
            pass
    
    if request.method == 'POST' and can_vote:
        choice_id = request.POST.get('choice')
        choice = get_object_or_404(Choice, id=choice_id, poll=poll)
        
        if user_vote:
            user_vote.choice = choice
            user_vote.save()
            messages.success(request, 'Ваш голос оновлено!')
        else:
            Vote.objects.create(user=request.user, poll=poll, choice=choice)
            messages.success(request, 'Дякуємо за участь у голосуванні!')
        
        return redirect('votes:vote_results', poll_id=poll.id)
    
    context = {
        'poll': poll,
        'can_vote': can_vote,
        'user_vote': user_vote,
    }
    return render(request, 'votes/vote_detail.html', context)

@user_passes_test(is_moderator_or_admin)
def vote_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        end_date = request.POST.get('end_date')
        
        poll = Poll.objects.create(
            title=title,
            description=description,
            created_by=request.user,
            end_date=end_date if end_date else None
        )
        
        choices_text = request.POST.getlist('choices')
        for text in choices_text:
            if text.strip():
                Choice.objects.create(poll=poll, text=text.strip())
        
        messages.success(request, 'Голосування успішно створено!')
        return redirect('votes:vote_detail', poll_id=poll.id)
    
    return render(request, 'votes/vote_form.html')

@user_passes_test(is_moderator_or_admin)
def vote_edit(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    
    if request.method == 'POST':
        poll.title = request.POST.get('title')
        poll.description = request.POST.get('description')
        poll.is_active = request.POST.get('is_active') == 'on'
        poll.end_date = request.POST.get('end_date') or None
        poll.save()
        
        poll.choices.all().delete()
        choices_text = request.POST.getlist('choices')
        for text in choices_text:
            if text.strip():
                Choice.objects.create(poll=poll, text=text.strip())
        
        messages.success(request, 'Голосування оновлено!')
        return redirect('votes:vote_detail', poll_id=poll.id)
    
    context = {'poll': poll}
    return render(request, 'votes/vote_form.html', context)

@user_passes_test(is_moderator_or_admin)
def vote_delete(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    if request.method == 'POST':
        poll.delete()
        messages.success(request, 'Голосування видалено!')
        return redirect('votes:vote_list')
    
    return render(request, 'votes/vote_confirm_delete.html', {'poll': poll})

def vote_results(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    total_votes = Vote.objects.filter(poll=poll).count()
    
    choices_data = []
    for choice in poll.choices.all():
        votes = choice.vote_set.count()
        if total_votes > 0:
            percentage = round((votes / total_votes * 100), 1)
        else:
            percentage = 0
        choices_data.append({
            'choice': choice,
            'votes': votes,
            'percentage': percentage,
        })
    
    context = {
        'poll': poll,
        'choices_data': choices_data,
        'total_votes': total_votes,
    }
    return render(request, 'votes/vote_results.html', context)