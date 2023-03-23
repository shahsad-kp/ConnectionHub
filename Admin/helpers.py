from django.contrib.auth.decorators import user_passes_test


def superuser_login_required(view_func=None, redirect_field_name=None, login_url=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator
