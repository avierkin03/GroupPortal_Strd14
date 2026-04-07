from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Material, Like
from materials.form import Materials_CreateForm, Material_FilterForm, ImageFormSet
from django.contrib.auth.mixins import LoginRequiredMixin
from materials.mixins import UserMaterial
from django.http import HttpResponseRedirect

# Create your views here.

#Список всіх матеріалів які зробив адмін
class Materials_ListView(ListView):
    model = Material
    context_object_name = "materials"
    template_name = "materials/material-list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get("category", "")
        if category:
            queryset = queryset.filter(category=category)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = Material_FilterForm(self.request.GET)
        return context

#Інфа про матеріал
class Materials_DatailView(DetailView):
    model = Material
    context_object_name = "material"
    template_name = "materials/material.html"

    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context["material_filefrom"] = Material_FileForm()
    #    return context


#Створити новий матеріал
class Materials_CreateView(LoginRequiredMixin, CreateView):
    model = Material
    template_name = "materials/material-form.html"
    form_class = Materials_CreateForm
    success_url = reverse_lazy("mater:material-list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            # Якщо не адмін — повертаємо на список матеріалів або видаємо помилку
            return redirect('mater:material-list') 
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.object or Material()
        if self.request.POST:
            context['formset'] = ImageFormSet(self.request.POST, self.request.FILES, instance=instance)
        else:
            context['formset'] = ImageFormSet(instance=instance)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save(commit=False)
            self.object.author = self.request.user
            self.object.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

        

#Редагувати матеріал
class Materials_UpdateView(LoginRequiredMixin, UpdateView):
    model = Material
    form_class = Materials_CreateForm
    template_name = "materials/material-form.html"
    success_url = reverse_lazy("mater:material-list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            # Якщо не адмін — повертаємо на список матеріалів або видаємо помилку
            return redirect('mater:material-list') 
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['formset'] = ImageFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        # Друкуємо для відладки в консоль (залиш для перевірки)
        print("FORMSET VALID:", formset.is_valid())
        if not formset.is_valid():
            print("FORMSET ERRORS:", formset.errors)

        if form.is_valid() and formset.is_valid():
            self.object = form.save() # Просто зберігаємо основну форму
            formset.instance = self.object
            formset.save()
            return redirect(self.get_success_url())
        
        return self.render_to_response(self.get_context_data(form=form))


#Видалети матеріал
class Materials_DeleteView(LoginRequiredMixin, DeleteView):
    model = Material
    template_name = "materials/material-delete.html"
    success_url = reverse_lazy("mater:material-list")

    def form_valid(self, form):
        form.instance.author = self.author.user
        return super().form_valid(form)

class Materials_CompleteView(LoginRequiredMixin, UserMaterial, View):
    def post(self, request, *args, **kwargs):
        materials = self.get_object()
        materials.status = "done"
        materials.save()
        return HttpResponseRedirect(reverse_lazy("mater:material-list"))

def Like_Material(request, pk):
    material = get_object_or_404(Material, id=pk)
    like_qs = Like.objects.filter(user=request.user, material=material)
    if like_qs.exists():
        like_qs.delete()  # Забрати лайк
    else:
        Like.objects.create(user=request.user, material=material)     # Поставити лайк
    return redirect('mater:material-dateil', pk=pk)

#def upload_file(request):
#    if request.method == 'POST':
#        form = Materials_CreateForm(request.POST, request.FILES) # request.FILES обов'язково
#        if form.is_valid():
#            material = form.save(commit=False)
#            material.author = request.user # Автоматично ставимо автора
#            material.save()
#            # Переконайся, що в urls.py є назва 'material-list'
#            return redirect('mater:material-list')
#    else:
#        form = Materials_CreateForm()
#    return render(request, 'material.html', {'form': form})
#from django.shortcuts import render

# Create your views here.

