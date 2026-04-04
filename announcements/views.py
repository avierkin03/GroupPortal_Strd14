from django.shortcuts import render
from django.views.generic import ListView,DetailView,CreateView,DeleteView
from .models import Announcement
from .forms import TaskForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin

# Create your views here.
class AnnouncementListViev(ListView):
    model = Announcement
    template_name = "announcements/announcements_list.html"
    context_object_name = "announcements"

class AnnouncementDetailedViev(DetailView):
    model = Announcement
    template_name = "announcements/announcements_detail.html"
    context_object_name = "announcement"

class AnnouncementCreateViev(UserPassesTestMixin,CreateView):
    model = Announcement
    template_name = "announcements/announcements_form.html"
    form_class = TaskForm
    success_url = reverse_lazy("announcements-list")
    def test_func(self):
        return self.request.user.profile.role == "admin"

class AnnouncementDeleteViev(UserPassesTestMixin,DeleteView):
    model = Announcement
    template_name = "announcements/announcements_delete.html"
    form_class = TaskForm
    success_url = reverse_lazy("announcements-list")
    def test_func(self):
        return self.request.user.profile.role == "admin"


