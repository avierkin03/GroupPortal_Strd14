from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_project, name="create_project"),
    path("delete/<int:id>/", views.delete_project, name="delete_project"),
    path("user/<str:username>/", views.user_projects, name="user_projects"),
]