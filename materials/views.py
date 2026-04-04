from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.forms import modelformset_factory
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Material, Like, Material_imgcustom
from materials.form import Materials_CreateForm, Material_FilterForm
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
    
    ImageFormSet = modelformset_factory(Material_imgcustom, fields=('image',), extra=3, max_num=3)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = self.ImageFormSet(self.request.POST, self.request.FILES, queryset=Material_imgcustom.objects.none())
        else:
            context['formset'] = self.ImageFormSet(queryset=Material_imgcustom.objects.none())
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        
        if formset.is_valid():
            # 1. Спочатку вказуємо автора
            form.instance.author = self.request.user
            # 2. Зберігаємо основний об'єкт Material
            self.object = form.save()

            # 3. Зберігаємо картинки, прив'язуючи їх до щойно створеного self.object
            instances = formset.save(commit=False)
            for instance in instances:
                instance.material = self.object
                instance.save()
            
            # 4. Тільки тепер викликаємо super(), який зробить успішний редірект
            return super().form_valid(form)
        else:
            # Якщо картинки не валідні, повертаємо користувача до форми
            return self.render_to_response(self.get_context_data(form=form))


#Редагувати матеріал
class Materials_UpdateView(LoginRequiredMixin, UpdateView):
    model = Material
    form_class = Materials_CreateForm
    template_name = "materials/material-form.html"
    success_url = reverse_lazy("mater:material-list")

    ImageFormSet = modelformset_factory(Material_imgcustom, fields=('image',), extra=1, max_num=3, can_delete=True)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Отримуємо картинки, які вже прив'язані до цього об'єкта
        qs = Material_imgcustom.objects.filter(material=self.object)
        
        if self.request.POST:
            context['formset'] = self.ImageFormSet(self.request.POST, self.request.FILES, queryset=qs)
        else:
            context['formset'] = self.ImageFormSet(queryset=qs)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        
        if formset.is_valid():
            # Зберігаємо зміни в самому матеріалі
            self.object = form.save()
            
            # Обробляємо картинки (нові, змінені або видалені)
            instances = formset.save(commit=False)
            
            # Видаляємо ті, що позначені галочкою "Delete"
            for obj in formset.deleted_objects:
                obj.delete()

            for instance in instances:
                instance.material = self.object
                instance.save()
                
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

#Видалети матеріал
class Materials_DeleteView(LoginRequiredMixin, DeleteView):
    model = Material
    template_name = "materials/material-delete.html"
    success_url = reverse_lazy("mater:material-list")

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

def upload_file(request):
    if request.method == 'POST':
        form = Materials_CreateForm(request.POST, request.FILES) # request.FILES обов'язково
        if form.is_valid():
            material = form.save(commit=False)
            material.author = request.user # Автоматично ставимо автора
            material.save()
            # Переконайся, що в urls.py є назва 'material-list'
            return redirect('mater:material-list')
    else:
        form = Materials_CreateForm()
    return render(request, 'material.html', {'form': form})