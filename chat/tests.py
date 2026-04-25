from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import ChatRoom, Message, Mute, ChatInvitation

class ChatModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.room = ChatRoom.objects.create(name='Test Room', room_type='general')

    def test_chat_room_creation(self):
        self.assertEqual(self.room.name, 'Test Room')
        self.assertEqual(self.room.room_type, 'general')
        self.assertFalse(self.room.is_private)

    def test_message_creation(self):
        message = Message.objects.create(room=self.room, sender=self.user, content='Hello!')
        self.assertEqual(message.content, 'Hello!')
        self.assertEqual(message.sender, self.user)
        self.assertEqual(message.room, self.room)
    
    def test_mute_creation(self):
        muted_user = User.objects.create_user(username='muted', password='12345')
        mute = Mute.objects.create(user=self.user, muted_user=muted_user)
        self.assertEqual(mute.user, self.user)
        self.assertEqual(mute.muted_user, muted_user)

class ChatViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.room = ChatRoom.objects.create(name='Test Room', room_type='general')

    def test_chat_home_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('chat:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Room')

    def test_send_message_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('chat:send_message', kwargs={'room_id': self.room.id}), {'content': 'Test message'})
        self.assertEqual(response.status_code, 302)  # Redirect after post
        self.assertTrue(Message.objects.filter(content='Test message').exists())
