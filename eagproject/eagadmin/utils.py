from django.template import RequestContext
from django.shortcuts import render_to_response

def admin_render(request, template_name, data):
    return render_to_response(template_name, data,
            context_instance=RequestContext(request))

