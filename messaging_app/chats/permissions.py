from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """
    
    def has_permission(self, request, view):
        # Allow only authenticated users to access the API
        if not request.user.is_authenticated:
            return False
        return True
    
    def has_object_permission(self, request, view, obj):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return False
            
        # Check if user is a participant in the conversation
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        elif hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()
        
        # Allow GET, POST, PUT, PATCH, DELETE only for participants
        if request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
            return request.user in obj.participants.all()
        
        return False

class IsMessageParticipant(permissions.BasePermission):
    """
    Custom permission to only allow participants to access messages.
    """
    
    def has_object_permission(self, request, view, obj):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return False
            
        # Check if user is sender or receiver of the message
        if request.method in ['GET', 'PUT', 'PATCH', 'DELETE']:
            return request.user == obj.sender or request.user == obj.receiver
        
        return True

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Write permissions are only allowed to the owner.
        return obj.sender == request.user