from django.urls import path
from . import views

app_name = 'faq'
urlpatterns = [
    path("",views.FAQ_ListView.as_view(),name='FAQ-list'),
    path("<int:pk>/", views.FAQ_DetailView.as_view(), name="FAQ-detail"),
    path('FAQ-create',views.FAQ_CreateView.as_view(),name='FAQ-create'),
    path('<int:pk>/update/',views.FAQ_UpdateView.as_view(),name='FAQ-update'),
    path('<int:pk>/delete/',views.FAQ_DeleteView.as_view(),name='FAQ-delete'),
]