from django.urls import path
from . import views

urlpatterns = [
    path('conversation/', views.conversation_messages, name='conversation_messages'),
    path('conversation/<uuid:conversation_id>/', views.conversation_messages, name='conversation_detail'),
    path('unread/', views.unread_messages, name='unread_messages'),
    path('thread/<uuid:message_id>/', views.threaded_conversation, name='threaded_conversation'),
    path('messages/', views.MessageListView.as_view(), name='message_list'),
]