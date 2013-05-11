from django.contrib.contenttypes.models import ContentType
from django import template


register = template.Library()


@register.assignment_tag(name="get_content_type")
def get_content_type(model):
    """
    Returns the ContentType instance associated with class model.
    """
    content_type = ContentType.objects.get_for_model(model)
    return content_type
