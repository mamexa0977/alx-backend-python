from datetime import datetime
import logging
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden
import time

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        logging.basicConfig(
            filename='requests.log',
            level=logging.INFO,
            format='%(message)s'
        )

    def __call__(self, request):
        user = request.user if hasattr(request, 'user') and getattr(request.user, 'is_authenticated', False) else 'Anonymous'
        logging.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        # Allow access only between 6 PM (18) and 9 PM (21)
        if current_hour < 18 or current_hour >= 21:
            return HttpResponseForbidden("Chat access is restricted between 6 PM and 9 PM.")
        response = self.get_response(request)
        return response

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_message_times = {}

    def __call__(self, request):
        if request.method == "POST":
            ip = self.get_client_ip(request)
            now = time.time()
            timestamps = self.ip_message_times.get(ip, [])
            timestamps = [t for t in timestamps if now - t < 60]
            if len(timestamps) >= 5:
                return HttpResponseForbidden("Message limit exceeded. Please wait before sending more messages.")
            timestamps.append(now)
            self.ip_message_times[ip] = timestamps
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)
        # Only check for authenticated users
        if user and user.is_authenticated:
            role = getattr(user, 'role', None)
            if role not in ['admin', 'moderator']:
                return HttpResponseForbidden("Access denied: insufficient role permissions.")
        response = self.get_response(request)
        return response
