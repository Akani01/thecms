from django.utils.deprecation import MiddlewareMixin


class LoginCheckMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Middleware logic here
        response = self.get_response(request)
        return response



class CircuitSubdomainMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split('.')
        subdomain = host[0] if len(host) > 2 else None

        if subdomain:
            try:
                request.circuit = Circuit.objects.get(slug=subdomain)
            except Circuit.DoesNotExist:
                request.circuit = None
        else:
            request.circuit = None

        return self.get_response(request)