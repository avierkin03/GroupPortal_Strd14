from django.urls import path
from .views import ChatHomeView, SendMessageView

app_name = 'chat'

urlpatterns = [
    path('', ChatHomeView.as_view(), name='home'),
    path('send/<int:room_id>/', SendMessageView.as_view(), name='send_message'),
]