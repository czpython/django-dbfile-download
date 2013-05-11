from django.conf.urls import patterns, include, url

from .views import download_file_from_obj

urlpatterns = patterns('',
    url(
    	r'^download/(?P<content_type>\d+)/(?P<object_id>.+)/$',
    	download_file_from_obj,
    	name='generic_file_download',
    ),
)
