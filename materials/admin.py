from django.contrib import admin
from .models import Material, Like, Material_imgcustom

# Register your models here.
admin.site.register(Material)

admin.site.register(Like)

admin.site.register(Material_imgcustom)

class MaterialImageInline(admin.TabularInline):
    model = Material_imgcustom
    extra = 3  # Кількість порожніх слотів для завантаження, які видно одразу

# Register your models here.
