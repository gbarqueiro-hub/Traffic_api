import logging
import time

logger = logging.getLogger('traffic_api')

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        logger.info(f"Request started: {request.method} {request.get_full_path()}")

        response = self.get_response(request)

        duration = time.time() - start_time
        logger.info(f"Request finished: {request.method} {request.get_full_path()} - Status: {response.status_code} - Duration: {duration:.2f}s")

        return response
