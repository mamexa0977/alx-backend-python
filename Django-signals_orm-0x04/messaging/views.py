from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages as django_messages
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
    # Using the custom manager to get unread messages with .only() optimization
    unread_messages = Message.unread.unread_for_user(request.user)
    return render(request, 'messaging/unread.html', {
        'unread_messages': unread_messages
    })

@login_required
def threaded_conversation(request, message_id):
    """Task 3: Threaded conversation with optimized ORM queries"""
    # Using prefetch_related and select_related with sender=request.user filter
    root_message = get_object_or_404(
        Message.objects.select_related('sender', 'receiver')
        .prefetch_related('replies__sender', 'replies__receiver')
        .filter(sender=request.user),  # Added sender=request.user filter
        id=message_id
    )
    
    return render(request, 'messaging/thread.html', {
        'root_message': root_message
    })

@login_required
def delete_user(request):
    """Task 2: Delete user account view"""
    if request.method == 'POST':
        user = request.user
        # Delete the user account
        user.delete()  # This will trigger the post_delete signal
        django_messages.success(request, 'Your account has been deleted successfully.')
        return redirect('login')
    
    return render(request, 'messaging/delete_user_confirm.html')

@login_required
def message_edit_history(request, message_id):
    """Display message edit history"""
    message = get_object_or_404(Message, id=message_id, sender=request.user)
    history = message.history.all().select_related('edited_by')
    
    return render(request, 'messaging/edit_history.html', {
        'message': message,
        'history': history
    })

# Class-based view with cache
@method_decorator(cache_page(60), name='dispatch')
class MessageListView(View):
    """Class-based view for messages with caching"""
    
    def get(self, request):
        # Using prefetch_related and select_related with sender filter
        messages = Message.objects.filter(
            sender=request.user  # Added sender=request.user filter
        ).select_related('sender', 'receiver').prefetch_related('replies')
        
        return render(request, 'messaging/message_list.html', {
            'messages': messages
        })