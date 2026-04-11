from django.urls import path
from . import views

app_name = 'votes'

urlpatterns = [
    path('', views.vote_list, name='vote_list'),
    path('<int:poll_id>/', views.vote_detail, name='vote_detail'),
    path('<int:poll_id>/results/', views.vote_results, name='vote_results'),
    path('create/', views.vote_create, name='vote_create'),
    path('<int:poll_id>/edit/', views.vote_edit, name='vote_edit'),
    path('<int:poll_id>/delete/', views.vote_delete, name='vote_delete'),
]