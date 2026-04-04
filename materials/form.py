from django import forms
from materials.models import Material

class Materials_CreateForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ["title", "description", "category", "file_type", "material_file", "material_url", "subtitle"]

        widgets = {
            'material_url': forms.URLInput(attrs={
                'placeholder': 'Add your link'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Робимо поле необов'язковим прямо у формі
        self.fields['subtitle'].required = False

    def __init__(self, *args, **kwargs):
        super(Materials_CreateForm, self).__init__(*args, **kwargs)
        # Додаємо клас для всіх полів
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
        
        # Перевір, чи поле "date" є у списку fields вище. 
        # Якщо його немає в Meta fields, цей рядок викличе помилку. 
        # Якщо воно є, виправ опечатку: "datepicker"
        if "date" in self.fields:
            self.fields["date"].widget.attrs["class"] += " my-custom-datepicker"


class Material_FilterForm(forms.Form):
    CATEGORY_CHOICES = [
        ('basics', 'Основи програмування'),
        ('web', 'WEB-розробка'),
        ('git', 'Git та GitHub'),
    ]
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=False, label="Категорія")

    def __init__(self, *args, **kwargs):
        super(Material_FilterForm, self).__init__(*args, **kwargs)
        self.fields["category"].widget.attrs.update({"class": "form-control"})
