import django_filters
from django_filters import rest_framework as filters
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageFilter(filters.FilterSet):
    conversation = filters.UUIDFilter(field_name='conversation__id')
    sender = filters.ModelChoiceFilter(queryset=User.objects.all())
    receiver = filters.ModelChoiceFilter(queryset=User.objects.all())
    timestamp_after = filters.DateTimeFilter(field_name='timestamp', lookup_expr='gte')
    timestamp_before = filters.DateTimeFilter(field_name='timestamp', lookup_expr='lte')
    read = filters.BooleanFilter()
    
    class Meta:
        model = Message
        fields = ['conversation', 'sender', 'receiver', 'read']