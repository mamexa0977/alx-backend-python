from datetime import datetime
import logging
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden
import time

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('requests.log')
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

class RequestLoggingMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous'
        log_entry = f"[{datetime.now()}] {request.method} {request.get_full_path()} by {user}"
        logger.info(log_entry)
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
