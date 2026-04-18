from django.urls import path
from . import views

app_name = 'diary'

urlpatterns = [
    path('grades/', views.GradeListView.as_view(), name='grade_list')
]