from apps.constant.common import LIMIT
from apps.filters import filters
from apps.models.blog import BlogCategory


@filters.app_context_processor
def render_category():
    # Query all category inside index page
    return dict(categories=BlogCategory.objects(external=True, removed=False).order_by('name').limit(LIMIT))
