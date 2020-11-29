from django.conf.urls.defaults import *

urlpatterns = patterns('eagadmin.views',
        url(r'^$', 'index', name='index'),
        url(r'^new$', 'new', name='new'),
        url(r'^add$', 'add', name='add'),
        url(r'^delete/(?P<page_key>\S+)$', 'delete', name='delete'),
        url(r'^edit/(?P<page_key>\S+)$', 'edit', name='edit'),
        url(r'^reorder$', 'reorder', name='reorder'),
        url(r'^type/(?P<page_key>\S+)$', 'type', name='type'),
        url(r'^picasa$', 'picasa', name='picasa-all'),
        url(r'^picasa/(?P<album>\S+)$', 'picasa', name='picasa-one'),
)

