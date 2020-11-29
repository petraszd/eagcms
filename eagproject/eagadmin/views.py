from eagadmin import types
types.load() # Preloads all pages.Page subclasses

from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from eagadmin.models import pages
from eagadmin.utils import admin_render
from eagadmin.forms import PageForm, TypeForm
from eagadmin.account import admin_required
from google.appengine.ext.db import djangoforms
from google.appengine.api import urlfetch, users
from django.conf import settings
import django.template
django.template.add_to_builtins('django.templatetags.i18n')

@admin_required
def index(request, form=None):
    data = {'tree': pages.get_all(),}
    return admin_render(request, 'eagadmin/index.html', data)

@admin_required
def new(request, form=None):
    if not form:
        form = PageForm()
    data = {'page_form': form}
    return admin_render(request, 'eagadmin/new.html', data)

@admin_required
def add(request):
    if not request.POST:
        raise Http404()
    form = PageForm(request.POST)
    if form.is_valid():
        top = pages.Page.get(form.cleaned_data['top'])
        type = form.cleaned_data['type']

        p = form.save(commit=False)
        pages.add_as_last_child(pages.to_type(p, type), top)
        return redirect('eagadmin:index')
    return new(request, form)

@admin_required
def delete(request, page_key):
    page = pages.Page.get(page_key)
    if not page: raise Http404()

    pages.delete_with_branch(page)
    return redirect('eagadmin:index')

@admin_required
def edit(request, page_key):
    page = pages.Page.get(page_key)
    if not page: raise Http404()

    form = PageForm((request.POST or None), instance=page)
    ContentForm = types.get_formclass(page)
    cform = ContentForm((request.POST or None), instance=page)

    if request.POST and form.is_valid() and cform.is_valid():
        page = form.save(commit=False)
        for k, v in cform.cleaned_data.iteritems():
            setattr(page, k, v)
        page.put()
    data = {'page': page, 'form': form, 'cform': cform}
    return admin_render(request, 'eagadmin/edit.html', data)

@admin_required
def reorder(request):
    try:
        serialized = request.POST['new_order']
    except KeyError:
        raise Http404()

    neworder = [p.split(' ') for p in serialized.split('&')]
    pages.reorder([(key, int(level)) for key, level in neworder])

    return redirect('eagadmin:index')

@admin_required
def picasa(request, album=None):
    nick = users.get_current_user().nickname()

    # Fall back to current user's nickname
    guser = getattr(settings, 'EAGCMS_PICASA_USER', nick)
    url = 'http://picasaweb.google.com/data/feed/api/user/%s' % guser
    if album:
        url += '/albumid/%s' % (str(album))
    url += '?alt=json&access=public'
    result = urlfetch.fetch(url)
    if result.status_code == 200:
        response = HttpResponse(result.content)
        response['GData-Version'] = '2'
        return response
    return HttpResponse("{}")

@admin_required
def type(request, page_key):
    page = pages.Page.get(page_key)
    if not page: raise Http404()

    if request.POST:
        form = TypeForm(request.POST)
        if form.is_valid():
            new_type = form.cleaned_data['type']
            newpage = pages.to_type(page, new_type)
            newpage.put()
            pages.reparent(page, newpage)
            page.delete()
            return redirect('eagadmin:index')
    else:
        form = TypeForm(initial={'type': page.class_name})

    data = {'page': page, 'form': form}
    return admin_render(request, 'eagadmin/type.html', data)

def site(request, slug=""):
    page = pages.get_by_slug(slug)
    if not page: raise Http404()

    return page.get_response(request)

