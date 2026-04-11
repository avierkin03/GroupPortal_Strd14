from django.urls import path
from . import views

urlpatterns = [
    path("announcements-list/",views.AnnouncementListViev.as_view(),name="announcements-list"),
    path("<int:pk>/", views.AnnouncementDetailedViev.as_view(), name="announcement-detail"),
    path("announcement-create/",views.AnnouncementCreateViev.as_view(),name="announcement-create"),
    path("<int:pk>/delete/", views.AnnouncementDeleteViev.as_view(), name="announcement-delete")
]