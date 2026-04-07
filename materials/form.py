from django import forms
from django.forms import inlineformset_factory
from materials.models import Material, Material_imgcustom

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
        super(Materials_CreateForm, self).__init__(*args, **kwargs)
        self.fields['subtitle'].required = False
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
    
ImageFormSet = inlineformset_factory(
    Material,
    Material_imgcustom,
    fields=('image',),
    extra=1,
    max_num=3,
    can_delete=True,
    validate_max=True
)



class Material_FilterForm(forms.Form):
    CATEGORY_CHOICES = [
        ('','Всі'),
        ('basics', 'Основи програмування'),
        ('web', 'WEB-розробка'),
        ('git', 'Git та GitHub'),
    ]
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=False, label="Категорія")

    def __init__(self, *args, **kwargs):
        super(Material_FilterForm, self).__init__(*args, **kwargs)
        self.fields["category"].widget.attrs.update({"class": "form-control"})
