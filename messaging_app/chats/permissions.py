from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Check if user is a participant in the conversation
        return request.user in obj.participants.all()

class IsMessageParticipant(permissions.BasePermission):
    """
    Custom permission to only allow participants to access messages.
    """
    
    def has_object_permission(self, request, view, obj):
        # Check if user is sender or receiver of the message
        return request.user == obj.sender or request.user == obj.receiver

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