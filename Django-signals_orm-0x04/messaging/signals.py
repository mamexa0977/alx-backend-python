from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    """Task 0: Create notification when new message is received"""
    if created:
        Notification.objects.create(
            user=instance.receiver, 
            message=instance
        )
        print(f"Notification created for {instance.receiver.username}")

@receiver(pre_save, sender=Message)
def log_message_history(sender, instance, **kwargs):
    """Task 1: Log message edits before saving"""
    if instance.pk:  # Only for existing messages (updates)
        try:
            original = Message.objects.get(pk=instance.pk)
            if original.content != instance.content:  # Content changed
                # Create history record with edited_by field
                MessageHistory.objects.create(
                    original_message=instance,
                    old_content=original.content,
                    edited_by=instance.sender  # Set edited_by to the message sender
                )
                instance.edited = True
                print(f"Message history logged for message {instance.id}")
        except Message.DoesNotExist:
            pass  # New message, no history to log

@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """Task 2: Clean up related data when user is deleted"""
    # Delete all messages sent or received by the user
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    
    # Delete all notifications for the user
    Notification.objects.filter(user=instance).delete()
    
    # Delete message history for messages sent by the user
    MessageHistory.objects.filter(original_message__sender=instance).delete()
    
    print(f"Cleaned up all data for user {instance.username}")