from django.urls import path
from . import views

urlpatterns = [
    path("", views.ForumListView.as_view(), name="forum-list"),
    path("forum-create/", views.ForumCreateView.as_view(), name="forum-create"),
    path("<int:pk>/comments/", views.CommentListView.as_view(), name="forum-comments"),
    path("<int:pk>/comment-create/", views.CommentCreateView.as_view(), name="forum-comments-create"),
    path("forum-create/", views.ForumCreateView.as_view(), name="forum-create"),
    path("<int:pk>/delete/", views.ForumDeleteView.as_view(), name="forum-delete"),    
]
