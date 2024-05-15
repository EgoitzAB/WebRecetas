from allauth_2fa.middleware import BaseRequire2FAMiddleware

class RequireSuperuser2FAMiddleware(BaseRequire2FAMiddleware):
    def require_2fa(self, request):
        # Requiere que los superusuarios tengan 2FA.
        return request.user.is_superuser
