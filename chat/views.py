from django.shortcuts import render
from django import forms
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from announcements import models
from .models import ChatRoom, Message, ChatInvitation
from django.shortcuts import get_object_or_404, redirect

class ChatHomeView(LoginRequiredMixin, ListView):
    model = ChatRoom
    template_name = 'index.html'
    context_object_name = 'rooms'

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

    def get_queryset(self):
        # только те чаты где есть юзер
        return ChatRoom.objects.filter(
            models.Q(is_private=False) & models.Q(members=self.request.user)
        ).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Если в URL передан ID комнаты, достаем её сообщения
        room_id = self.request.GET.get('room')
        if room_id:
            current_room = get_object_or_404(ChatRoom, id=room_id)
            context['current_room'] = current_room
            # Фильтруем сообщения 
            muted_users = self.request.user.muted_by.values_list('muted_user', flat=True)
            context['chat_messages'] = current_room.messages.exclude(sender__id__in=muted_users)
        return context


class SendMessageView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm

    def form_valid(self, form):
        content = form.cleaned_data['content']
        room_id = self.kwargs.get('room_id')
        room = get_object_or_404(ChatRoom, id=room_id)
        
        #   ЛОГИКА КОМАНД
        if content.startswith('/mute '):
            username = content.replace('/mute @', '').strip()
            # Логика мута юзера
            return redirect('chat:home') 

        if content.startswith('/create_group '):
            # Логика создания группы и инвайта
            pass

        # Обычное сохранение сообщения
        form.instance.sender = self.request.user
        form.instance.room = room
        return super().form_valid(form)