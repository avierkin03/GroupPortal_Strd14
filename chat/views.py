from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q  # 
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from .models import ChatRoom, Message, ChatInvitation, Mute

# Форма для соо сообщения
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'placeholder': 'Напишите сообщение...', 'class': 'form-control'})
        }

class ChatHomeView(LoginRequiredMixin, ListView):
    model = ChatRoom
    template_name = 'chat/index.html' 
    context_object_name = 'rooms'

    def get_queryset(self):
        # Показываем публичные чаты или где юзер состоит в участниках
        return ChatRoom.objects.filter(
            Q(is_private=False) | Q(members=self.request.user)
        ).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room_id = self.request.GET.get('room')
        
        if room_id:
            current_room = get_object_or_404(ChatRoom, id=room_id)
            context['current_room'] = current_room
            
            # Список тех, кого текущий юзер замутил
            muted_users = Mute.objects.filter(user=self.request.user).values_list('muted_user', flat=True)
            
            # Сообщения комнаты, исключая замученных
            context['chat_messages'] = current_room.messages.exclude(sender__id__in=muted_users)
            context['form'] = MessageForm()
        return context

class SendMessageView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm

    def form_valid(self, form):
        content = form.cleaned_data['content'].strip()
        room_id = self.kwargs.get('room_id')
        room = get_object_or_404(ChatRoom, id=room_id)

        # 1. Проверка на право писать (для канала ИНФО)
        if not room.can_user_post(self.request.user):
            
            return redirect(f'/chat/?room={room_id}')

        # 2. Обработка команды /mute
        if content.startswith('/mute @'):
            target_username = content.replace('/mute @', '').strip()
            target_user = User.objects.filter(username=target_username).first()
            if target_user:
                Mute.objects.get_or_create(user=self.request.user, muted_user=target_user)
            return redirect(f'/chat/?room={room_id}')

        # 3. Обработка команды /create_group
        if content.startswith('/create_group @'):
            target_username = content.replace('/create_group @', '').strip()
            target_user = User.objects.filter(username=target_username).first()
            if target_user:
                # Создаение приват румы
                new_room = ChatRoom.objects.create(
                    name=f"Группа: {self.request.user} и {target_user}",
                    room_type='group',
                    is_private=True
                )
                new_room.members.add(self.request.user)
                # инвайт
                ChatInvitation.objects.create(
                    sender=self.request.user,
                    receiver=target_user,
                    room=new_room
                )
            return redirect(f'/chat/?room={room_id}')

        # Обычное сохранение сообщения
        form.instance.sender = self.request.user
        form.instance.room = room
        form.save()
        return redirect(f'/chat/?room={room_id}')