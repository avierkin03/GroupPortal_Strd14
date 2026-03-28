from django.db import models
from django.contrib.auth.models import User

class ChatRoom(models.Model):
    # Название для групповых чатов
    main_chat = models.CharField(max_length=255, null=True, blank=True)
    
    # Флаг для определения соо идет в лс или в
    is_private = models.BooleanField(default=False)
    
    # Список участников (для ЛС тут будет ровно двое)
    members = models.ManyToManyField(User, related_name='chat_rooms')

    def __str__(self):
        return self.name if self.name else f"Chat {self.id} (Private)"

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class ChatRoom(models.Model):
    ROOM_TYPES = (
        ('general', 'Общий'),
        ('problems', 'Ошибки и решения'),
        ('memes', 'Мемы'),
        ('info', 'Инфо (Только админы)'),
        ('private', 'Личный чат'),
        ('group', 'Групповой чат'),
    )
    name = models.CharField(max_length=255)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, default='general')
    members = models.ManyToManyField(User, related_name='chat_rooms')

class Mute(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='muted_by')
    muted_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='is_muted_by')

class ChatInvitation(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invites')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_invites')
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=(('pending', 'Ожидание'), ('accepted', 'Принято'), ('declined', 'Отклонено')), default='pending')

    def can_user_post(self, user):
        if self.room_type == 'info':
            return user.is_staff or user.groups.filter(name='Moderators').exists()
        return True

    class Meta:
        ordering = ['timestamp'] # Чтобы соо шли по порядку

    def __str__(self):
        return f'{self.sender.username}: {self.content[:20]}'