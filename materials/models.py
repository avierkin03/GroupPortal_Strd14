from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Material(models.Model):
    CATEGORY_CHOICES = [
        ('basics', 'Основи програмування'),
        ('web', 'WEB-розробка'),
        ('git', 'Git та GitHub'),
    ]

    TYPE_CHOICES = [
        ("video", "Відео"),
        ("file", "Файл"),
        ("img", "Картинка"),
    ]

    title = models.CharField(max_length=256)#Заголовок
    description = models.TextField()#опис
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=100, default='basics')#категорія
    file_type = models.CharField(choices=TYPE_CHOICES, max_length=100, default='video')#тип файлу
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="materials")#автор матеріалу
    material_file = models.FileField(upload_to='materials_media/',  null=True, blank=True)#файл
    material_date = models.DateTimeField(auto_now_add=True)#дата створення
    material_url = models.URLField(max_length=500, null=True, blank=True)#силка
    subtitle = models.TextField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.title} "
    

#Клас для картинок
#Дати вибір скільки картинок хоче адмін додати до матеріалу
class Material_imgcustom(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='materials_media/images/')
    def __str__(self):
        return f"{self.material.title}"

#Клас лайку 
#Дати змогу оцінити матеріал
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Цей рядок робить так, щоб один юзер міг лайкнути один матеріал лише 1 раз
        unique_together = ('user', 'material')

    def total_likes(self):
        return self.likes.count()
#python manage.py runserver