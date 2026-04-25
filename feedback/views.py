from django.views.generic import CreateView, ListView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from .models import Feedback
from .forms import FeedbackForm
from django.db.models import Avg, Count
from django.views.generic import ListView


class PublicFeedbackListView(ListView):
    model = Feedback
    template_name = 'feedback/public_feedback.html'
    context_object_name = 'feedbacks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['avg_rating'] = Feedback.objects.aggregate(Avg('rating'))['rating__avg']
        context['count'] = Feedback.objects.aggregate(Count('id'))['id__count']
        return context


class FeedbackCreateView(CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'feedback/feedback_form.html'
    success_url = reverse_lazy('feedback_thanks')


class FeedbackThanksView(TemplateView):
    template_name = 'feedback/feedback_thanks.html'


class FeedbackListView(UserPassesTestMixin, ListView):
    model = Feedback
    template_name = 'feedback/feedback_list.html'
    context_object_name = 'feedbacks'

    def test_func(self):
        return self.request.user.is_staff


class UnreadFeedbackListView(UserPassesTestMixin, ListView):
    model = Feedback
    template_name = 'feedback/feedback_list.html'
    context_object_name = 'feedbacks'

    def get_queryset(self):
        return Feedback.objects.filter(is_read=False)

    def test_func(self):
        return self.request.user.is_staff

def mark_as_read(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk)
    feedback.is_read = True
    feedback.save()
    return redirect('feedback_list')
