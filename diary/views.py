from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Grade
from django.contrib.auth.mixins import LoginRequiredMixin


class GradeListView(LoginRequiredMixin, ListView):
    model = Grade
    template_name = 'diary/grade_list.html'
    context_object_name = 'grades'

    def get_queryset(self):
        return self.request.user.profile.grades.order_by('-date')
    

class GradeCreateView(CreateView):
    model = Grade
    fields = ["student", "logic_points"]
    template_name = "students/grade_form.html"

    def get_success_url(self):
        return reverse_lazy("student_detail", kwargs={"pk": self.object.student.pk})