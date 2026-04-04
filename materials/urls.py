from django.urls import path
from . import views

app_name = "mater"

urlpatterns = [
    path("materials/", views.Materials_ListView.as_view(), name="material-list"),
    path("material/<int:pk>/", views.Materials_DatailView.as_view(), name="material-dateil"),
    path("material-create/", views.Materials_CreateView.as_view(), name="material-create"),
    path("materials/<int:pk>/update/", views.Materials_UpdateView.as_view(), name="material-update"),
    path("materials/<int:pk>/delete/", views.Materials_DeleteView.as_view(), name="material-delete"),
    path("like/<int:pk>/", views.Like_Material, name="material-like"),

]