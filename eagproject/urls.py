from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^admin/', include('eagadmin.urls', namespace='eagadmin')),
    (r'^admin', include('eagadmin.urls', namespace='eagadmin')),
    (r'^(.*)$', 'eagadmin.views.site')


    # You need that duplication of 'admin' 'admin/' because
    # last regexp matches everything and does not allow
    # CommonMiddleware to add '/' and the end.
    # Below code demonstrates regexps without (.*) pattern.

    #(r'^admin/', include('eagadmin.urls', namespace='eagadmin')),
    #(r'^site/(.*)$', 'eagadmin.views.site')
)

