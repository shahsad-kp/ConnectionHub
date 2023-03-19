class ThemeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'preferred_theme' not in request.COOKIES:
            pass
            # response = self.get_response(request)
            # response.set_cookie('preferred_theme', 'dark' if self.is_preferred_theme_dark(request) else 'light')
        else:
            request.session['preferred_theme'] = request.COOKIES['preferred_theme']
        return self.get_response(request)

    def is_preferred_theme_dark(self, request):
        if request.META.get('HTTP_USER_AGENT') is not None and 'Macintosh' in request.META.get('HTTP_USER_AGENT'):
            # On macOS, the system default is light, so we assume the user prefers dark mode.
            return True
        else:
            # On other operating systems or browsers, we use the system default.
            return request.META.get('HTTP_ACCEPT') is not None and 'dark' in request.META.get('HTTP_ACCEPT')
