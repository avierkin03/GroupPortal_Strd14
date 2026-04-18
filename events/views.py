from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Event
from .forms import EventForm

def is_admin_or_moderator(user):
    return user.is_staff


def event_list(request):
    events = Event.objects.all().order_by('date')
    return render(request, 'events/event_list.html', {'events': events})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})


@login_required
@user_passes_test(is_admin_or_moderator)
def event_create(request):
    form = EventForm(request.POST or None)
    if form.is_valid():
        event = form.save(commit=False)
        event.created_by = request.user
        event.save()
        return redirect('event_list')
    return render(request, 'events/event_form.html', {'form': form})


@login_required
@user_passes_test(is_admin_or_moderator)
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('event_detail', pk=pk)
    return render(request, 'events/event_form.html', {'form': form})


@login_required
@user_passes_test(is_admin_or_moderator)
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})