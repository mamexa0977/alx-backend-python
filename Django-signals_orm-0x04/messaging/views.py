from django.views.decorators.cache import cache_page
from django.shortcuts import render
from .models import Message

@cache_page(60)
def message_list(request):
    messages = Message.objects.all()
    return render(request, 'messages.html', {'messages': messages})