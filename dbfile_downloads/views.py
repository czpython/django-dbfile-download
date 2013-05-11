import mimetypes
from os.path import basename

from django.conf import settings
from django.http import HttpResponse, Http404
from django.core.exceptions import (
    ImproperlyConfigured,
    ObjectDoesNotExist,
)
from django.contrib.contenttypes.models import ContentType

try:
    ALLOWED_FILE_DOWNLOAD_MODELS = getattr(settings, 'ALLOWED_FILE_DOWNLOAD_MODELS')
except AttributeError, e:
    raise ImproperlyConfigured('Please define ALLOWED_FILE_DOWNLOAD_MODELS in your settings.')


def download_file_from_obj(request, content_type, object_id):
    try:
        content_type = ContentType.objects.get_for_id(content_type)
        obj = content_type.get_object_for_this_type(pk=object_id)
    except ObjectDoesNotExist, e:
        raise Http404
    module = '%s.%s' % (content_type.app_label, content_type.model)
    param = request.GET.get('param', 'file')
    if module in ALLOWED_FILE_DOWNLOAD_MODELS and hasattr(obj, param):
        generic_file = getattr(obj, param)
        content_type = mimetypes.guess_type(generic_file.name)[0]
        response = HttpResponse(generic_file, content_type=content_type)
        response['Content-Disposition'] = 'attachment; filename=%s' % basename(generic_file.path)
        response['Content-Length'] = generic_file.size
        return response
    raise Http404
    
