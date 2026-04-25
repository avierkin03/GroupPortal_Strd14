from django.db import models
from django.contrib.auth.models import User

class ChatRoom(models.Model):
    ROOM_TYPES = (
        ('general', 'Общий'),
        ('problems', 'Ошибки и решения'),
        ('memes', 'Мемы'),
        ('info', 'Инфо (Только админы)'),
        ('private', 'Личный чат'),
        ('group', 'Групповой чат'),
    )
    
    name = models.CharField(max_length=255, verbose_name="Название комнаты")
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, default='general')
    is_private = models.BooleanField(default=False)
    members = models.ManyToManyField(User, related_name='chat_rooms', blank=True)

    def __str__(self):
        return f"{self.name} ({self.get_room_type_display()})"

    def can_user_post(self, user):
        """Проверяет, может ли пользователь писать в этот канал"""
        if self.room_type == 'info':
            return user.is_staff or user.is_superuser
        return True

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp'] # Сообщения идут от старых к новым

    def __str__(self):
        return f'{self.sender.username}: {self.content[:20]}'

class Mute(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='muted_by_list')
    muted_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='is_muted_for')

    def __str__(self):
        return f"{self.user.username} замутил {self.muted_user.username}"

class ChatInvitation(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Ожидание'),
        ('accepted', 'Принято'),
        ('declined', 'Отклонено'),
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invites')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_invites')
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Invite from {self.sender} to {self.receiver} for {self.room.name}"