from django.shortcuts import render
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import FAQ_model
from django.urls import reverse_lazy
from .forms import FAQ_Form_CRT,FAQ_Form_UPD

# Create your views here.
class FAQ_ListView(ListView):
    model = FAQ_model
    context_object_name = 'FAQS'
    template_name = 'faq/all/FAQ_list.html'


class FAQ_DetailView(DetailView):
    model = FAQ_model 
    context_object_name = "FAQ"
    template_name = "faq/all/FAQ_detail.html"


class FAQ_CreateView(LoginRequiredMixin,CreateView):
    model = FAQ_model
    template_name = 'faq/all/FAQ.form.create.html'
    form_class = FAQ_Form_CRT
    success_url = reverse_lazy('faq:FAQ-list')
    def form_valid(self,form):
        form.instance.Questioner = self.request.user
        return super().form_valid(form)


class FAQ_UpdateView(UpdateView):
    model = FAQ_model
    template_name = 'faq/all/FAQ.form.update.html'
    form_class = FAQ_Form_UPD
    success_url = reverse_lazy('faq:FAQ-list')


class FAQ_DeleteView(DeleteView):
    model = FAQ_model
    template_name = 'faq/all/FAQ_delete.html'
    success_url = reverse_lazy('faq:FAQ-list')