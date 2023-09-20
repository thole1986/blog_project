from apps import cache
from apps.models import Province


@cache.cached(key_prefix='all_provinces')
def get_all_provinces():
    return Province.objects()


cached_provinces = get_all_provinces()
