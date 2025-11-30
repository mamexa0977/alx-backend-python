from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.decorators import login_required
from .models import Message, Notification

# Task 5: Cached view for messages
@cache_page(60)  # 60 seconds cache
@login_required
def conversation_messages(request, conversation_id=None):
    """View to display messages in a conversation with caching"""
    if conversation_id:
        # Get specific conversation with optimized queries
        messages = Message.objects.filter(
            parent_message__isnull=True
        ).prefetch_related(
            'replies', 'replies__sender', 'replies__receiver'
        ).select_related('sender', 'receiver')
    else:
        # Get all messages for user with optimization
        messages = Message.objects.filter(
            receiver=request.user
        ).select_related('sender').prefetch_related('replies')
    
    return render(request, 'messaging/conversation.html', {
        'messages': messages,
        'conversation_id': conversation_id
    })

@login_required
def unread_messages(request):
    """View using custom manager for unread messages"""
    # Using the custom manager to get unread messages
    unread_messages = Message.unread.for_user(request.user)
    return render(request, 'messaging/unread.html', {
        'unread_messages': unread_messages
    })

@login_required
def threaded_conversation(request, message_id):
    """Task 3: Threaded conversation with optimized ORM queries"""
    root_message = get_object_or_404(Message, id=message_id)
    
    # Optimized query using prefetch_related and select_related
    messages = Message.objects.filter(
        id=message_id
    ).prefetch_related(
        'replies__replies__replies'  # Multiple levels of replies
    ).select_related(
        'sender', 'receiver'
    ).first()
    
    return render(request, 'messaging/thread.html', {
        'root_message': messages
    })

# Class-based view with cache
@method_decorator(cache_page(60), name='dispatch')
class MessageListView(View):
    """Class-based view for messages with caching"""
    
    def get(self, request):
        messages = Message.objects.filter(receiver=request.user).select_related('sender')
        return render(request, 'messaging/message_list.html', {
            'messages': messages
        })