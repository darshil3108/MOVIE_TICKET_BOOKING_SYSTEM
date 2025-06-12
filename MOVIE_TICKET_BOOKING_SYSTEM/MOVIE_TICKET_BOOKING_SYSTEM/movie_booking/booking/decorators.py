from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def admin_required(function):
    """Decorator to require admin/staff privileges."""
    def check_admin(user):
        return user.is_authenticated and (user.is_staff or user.is_superuser)
    
    actual_decorator = user_passes_test(check_admin)
    return actual_decorator(function)

def superuser_required(function):
    """Decorator to require superuser privileges."""
    def check_superuser(user):
        return user.is_authenticated and user.is_superuser
    
    actual_decorator = user_passes_test(check_superuser)
    return actual_decorator(function)
