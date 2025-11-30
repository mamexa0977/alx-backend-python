from django.db import models

class UnreadMessagesManager(models.Manager):
    """Custom manager for unread messages"""
    
    def unread_for_user(self, user):
        """Filter unread messages for specific user"""
        return self.filter(receiver=user, read=False).only(
            'id', 'content', 'timestamp', 'sender__username', 'sender__id'
        )