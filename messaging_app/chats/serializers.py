from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'role', 'created_at', 'password']
        read_only_fields = ['user_id', 'created_at']
        extra_kwargs = {'password': {'write_only': True}}

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    message_body = serializers.CharField()  # Explicit CharField
    
    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation', 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sent_at']

    def validate_message_body(self, value):
        """Add validation to use ValidationError"""
        if not value or value.strip() == '':
            raise serializers.ValidationError("Message body cannot be empty")
        return value

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()  # Add SerializerMethodField
    
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at', 'message_count']
        read_only_fields = ['conversation_id', 'created_at']

    def get_message_count(self, obj):
        """SerializerMethodField implementation"""
        return obj.messages.count()