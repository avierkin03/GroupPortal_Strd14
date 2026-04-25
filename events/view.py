from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Event
from .forms import EventForm

class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('events')