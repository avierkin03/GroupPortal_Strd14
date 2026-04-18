from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.EventListView.as_view(), name="events"),
    path("create/", views.EventCreateView.as_view(), name="event_create"),
    path("<int:pk>/edit/", views.EventUpdateView.as_view(), name="event_edit"),
    path("<int:pk>/delete/", views.EventDeleteView.as_view(), name="event_delete"),
]
urlpatterns = [
    path('events/', include('events.urls')),

    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]