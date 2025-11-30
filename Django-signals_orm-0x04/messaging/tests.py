from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory
from .signals import create_message_notification, log_message_history, cleanup_user_data

class SignalTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('user1', 'user1@test.com', 'password')
        self.user2 = User.objects.create_user('user2', 'user2@test.com', 'password')

    def test_message_notification_signal(self):
        """Test that notification is created when message is sent"""
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Test message"
        )
        
        # Check if notification was created
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.user2)
        self.assertEqual(notification.message, message)

    def test_message_edit_history(self):
        """Test that message history is logged when message is edited"""
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Original content"
        )
        
        # Edit the message
        message.content = "Edited content"
        message.save()
        
        # Check if history was created
        self.assertEqual(MessageHistory.objects.count(), 1)
        history = MessageHistory.objects.first()
        self.assertEqual(history.old_content, "Original content")

class ORMTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('user1', 'user1@test.com', 'password')
        self.user2 = User.objects.create_user('user2', 'user2@test.com', 'password')

    def test_unread_messages_manager(self):
        """Test custom manager for unread messages"""
        # Create read and unread messages
        Message.objects.create(sender=self.user1, receiver=self.user2, content="Unread 1", read=False)
        Message.objects.create(sender=self.user1, receiver=self.user2, content="Unread 2", read=False)
        Message.objects.create(sender=self.user1, receiver=self.user2, content="Read 1", read=True)
        
        # Test custom manager
        unread_count = Message.unread.for_user(self.user2).count()
        self.assertEqual(unread_count, 2)

    def test_threaded_conversation(self):
        """Test threaded conversation with replies"""
        parent = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Parent message"
        )
        
        reply1 = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content="Reply 1",
            parent_message=parent
        )
        
        reply2 = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Reply 2", 
            parent_message=parent
        )
        
        # Test relationships
        self.assertEqual(parent.replies.count(), 2)
        self.assertEqual(reply1.parent_message, parent)