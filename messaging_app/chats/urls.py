from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet

# Using DefaultRouter for automatic URL routing
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet)
router.register(r'messages', MessageViewSet)

# Note: NestedDefaultRouter would require drf-nested-routers package
# For this assignment, we're using DefaultRouter as specified

urlpatterns = [
    path('', include(router.urls)),
]