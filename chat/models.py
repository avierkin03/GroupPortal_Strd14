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

    class Meta:
        ordering = ['timestamp'] # Чтобы соо шли по порядку

    def __str__(self):
        return f'{self.sender.username}: {self.content[:20]}'