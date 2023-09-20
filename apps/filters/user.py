from apps.constant.common import ZERO_VALUE
from apps.filters import filters
from apps.models import AnonymousUser, Role


@filters.app_template_filter()
def check_menus(user, menu):
    if isinstance(user, AnonymousUser):
        return False
    return len(list(set(user.roles).intersection(menu.roles))) > ZERO_VALUE


@filters.app_template_filter()
def check_role(user, role_list):
    """
    :param user: an instance of the User class
    :param role_list: a list of role name to check
    :return: True if any of user.roles is in the role_list
    """
    if isinstance(user, AnonymousUser):
        return False
    if not isinstance(role_list, list):
        return False
    if user.has_role('Admin'):
        return True
    if isinstance(role_list[0], Role):
        roles = Role.objects(id__in=[str(rol_obj.id) for rol_obj in role_list])
    else:
        roles = Role.objects(name__in=role_list)
    return len(list(set(roles).intersection(user.roles))) > ZERO_VALUE
