from apps.models import UserMenu


def render_menu():
    return UserMenu.objects(removed=False)
