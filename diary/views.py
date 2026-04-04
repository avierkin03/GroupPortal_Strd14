from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Student, Grade


class StudentListView(ListView):
    model = Student
    context_object_name = "students"
    template_name = "students/student_list.html"


class StudentDetailView(DetailView):
    model = Student
    context_object_name = "student"
    template_name = "students/student_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.object

        context["grades"] = student.grades.all()
        context["total_logics"] = student.total_logics()
        context["total_money"] = student.total_money()

        return context


class GradeCreateView(CreateView):
    model = Grade
    fields = ["student", "logic_points"]
    template_name = "students/grade_form.html"

    def get_success_url(self):
        return reverse_lazy("student_detail", kwargs={"pk": self.object.student.pk})