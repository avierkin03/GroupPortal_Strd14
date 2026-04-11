from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from .models import Vote, Choice, UserVote
from django.contrib.auth.decorators import login_required

def vote_list(request):
    votes = Vote.objects.all()
    return render(request, 'voting/vote_list.html', {'votes': votes})

@login_required
def vote_detail(request, vote_id):
    vote = get_object_or_404(Vote, id=vote_id)

    if request.method == 'POST':
        choice_id = request.POST.get('choice')
        choice = get_object_or_404(Choice, id=choice_id)
        UserVote.objects.update_or_create(
            user=request.user,
            vote=vote,
            defaults={'choice': choice}
        )
        return redirect('vote_list')

    return render(request, 'voting/vote_detail.html', {'vote': vote})
