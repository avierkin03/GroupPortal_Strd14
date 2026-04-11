from django.urls import path
from . import views

urlpatterns = [
    path('', views.vote_list, name='vote_list'),
    path('<int:vote_id>/', views.vote_detail, name='vote_detail'),
    path('<int:vote_id>/results/', views.vote_results, name='vote_results'),
]