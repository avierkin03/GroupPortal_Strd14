from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ForumForm, CommentForm
from .models import Forum, Comment
# Create your views here.

class ForumListView(LoginRequiredMixin, ListView):
    model = Forum
    context_object_name = "forums"
    template_name = "forum/forum_list.html"

class ForumCreateView(CreateView):
    model = Forum
    template_name = "forum/forum_form.html"
    form_class = ForumForm
    success_url = reverse_lazy("forum-list")

    # перевизначаємо метод form_valid
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CommentListView(ListView):
    model = Comment
    context_object_name = "comments"
    template_name = "forum/comment_list.html"

    def get_queryset(self):
        self.forum = get_object_or_404(Forum, pk=self.kwargs["pk"])
        return Comment.objects.filter(forum=self.forum)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["forum"] = self.forum
        return context
    
class CommentCreateView(CreateView):
    model = Comment
    template_name = "forum/comment_form.html"
    form_class = CommentForm
    success_url = reverse_lazy("forum-comments")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["forum"] = get_object_or_404(Forum, pk=self.kwargs["pk"])
        return context

    # перевизначаємо метод form_valid
    def form_valid(self, form):
        form.instance.owner = self.request.user
        forum = get_object_or_404(Forum, pk=self.kwargs["pk"])
        form.instance.forum = forum
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("forum-comments", kwargs={"pk": self.kwargs["pk"]})
    
class ForumDeleteView(DeleteView):
    model = Forum
    template_name = "forum/forum_delete.html"
    success_url = reverse_lazy("forum-list")

