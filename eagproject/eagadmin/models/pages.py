from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.db import polymodel
from eagadmin.types import get_types
from django.shortcuts import render_to_response
from django.template import TemplateDoesNotExist, RequestContext
from django.core.urlresolvers import reverse
# TODO: check all posible 'more than 1000' cases

# Not sure about tree construction in
# get_descendants, get_branch, get_all
# It is possible that all these functions
# just makes too many datastore calls
#
# Maybe (just maybe) it should fetch all
# pages at the beginning, parse it,
# construct tree and forget datastore

def _draft_filter(func):
    """ Decorator prevents acsesing draft pages """
    def newfunc(*args, **kwargs):
        ret = func(*args, **kwargs)

        user = users.get_current_user()
        if user or not ret:
            return ret

        if hasattr(ret, 'draft'):
            if ret.draft:
                return None
            return ret
        elif hasattr(ret, 'filter'):
            return ret.filter('draft =', False)
        return [p for p in ret if not p.draft]
    return newfunc

def get_root():
    root = Page.all().filter('level =', 0).get()
    if root:
        return root
    return add_root()

def choices():
    for p in get_all():
        yield (str(p.key()), unicode(p))

def get_all():
    root = get_root()
    return [root,] + get_descendants(root)

def get_branch(page):
    return get_descendants(page)

@_draft_filter
def get_children(page):
    return Page.all().filter('top =', page.key()).order('order')

@_draft_filter
def get_prev(page):
    return Page.all() \
            .filter('top =', page.top.key()) \
            .filter('order =', page.order - 1)

@_draft_filter
def get_next(page):
    return Page.all() \
            .filter('top =', page.top.key()) \
            .filter('order =', page.order + 1)

@_draft_filter
def get_by_slug(slug=''):
    if slug:
        return Page.all().filter('slug =', slug).get()
    return get_root()

def get_descendants(page, depth=-1):
    if depth == 0:
        return []
    if depth != -1:
        depth -= 1
    pages = []
    for c in get_children(page):
        pages += [c] + get_descendants(c, depth)
    return pages

@_draft_filter
def get_breadcrumb(page):
    tops = []
    top = page
    while True:
        if not top:
            break
        tops.append(top)
        top = top.top
    return list(reversed(tops))

def add_as_last_child(page, destination):
    try:
        last_child = list(destination.children)[-1]
        page.order = last_child.order + 1
    except IndexError:
        page.order = 0
    page.level = destination.level + 1
    page.top = destination.key()
    page.put()

def add_root():
    root = Page(top=None,
                 title='Home Page',
                 menu_name='Home',
                 slug='home-page')
    root.put()
    return root

def delete_with_branch(page):
    branch = get_branch(page)
    for p in branch:
        p.delete()
    q = Page.all() \
            .filter('top =', page.top.key()) \
            .filter('order >', page.order)
    for p in q:
        p.order -= 1
        p.put()
    page.delete()

def reorder(neworder):
    """
    neworder must be [(key, level), (key, level), ..]
    """
    all = get_all()
    top = all[0]
    pages = dict(((str(p.key()), p) for p in all[1:]))

    if len(pages) != len(neworder):
        raise ValueError("Lengths are not equal")

    prev_level = 1 # First elem's below root
    prev_page = top
    orders = [0,]
    tops = [top,]
    for key, level in neworder:
        page = pages[key]

        if level > prev_level:
            tops.append(prev_page), orders.append(0)
        elif level < prev_level:
            # It can go up more than one step
            for i in range(prev_level - level):
                tops.pop(), orders.pop()

        page.top = tops[-1]
        page.level = level
        page.order = orders[-1]

        page.put()

        orders[-1] += 1
        prev_page = page
        prev_level = level

def to_type(page, newtype):
    fields = page.fields()
    args = ((k, getattr(page, k)) for k, v in fields.iteritems())
    return get_types()[newtype].modelcl(**dict(args))

def reparent(old_parent, new_parent):
    for c in old_parent.children_set:
        c.top = new_parent
        c.put()

class Page(polymodel.PolyModel):
    top = db.SelfReferenceProperty(collection_name='children_set')
    order = db.IntegerProperty(required=True, default=0)
    level = db.IntegerProperty(required=True, default=0)

    title = db.StringProperty(required=True)
    slug = db.StringProperty(required=True)
    menu_name = db.StringProperty()
    draft = db.BooleanProperty()

    keywords = db.TextProperty()
    description = db.TextProperty()

    updated_at = db.DateTimeProperty(auto_now=True)
    updated_by = db.UserProperty(auto_current_user=True)

    @property
    def menu_title(self):
        if self.menu_name:
            return self.menu_name
        return self.title

    def is_root(self):
        return self.top == None

    def is_leaf(self):
        return len(self.children_set) == 0

    def has_top(self):
        return (not self.is_root())

    def has_children(self):
        return (not self.is_leaf())

    def has_next(self):
        return (not self.get_next())

    def has_prev(self):
        return (not self.get_prev())

    def get_response(self, request):
        data = {
            'current': self,
            'breadcrumb': get_breadcrumb(self)
        }
        tname = 'eagsite/types/%s.html' % self.class_name().lower()
        try:
            return render_to_response(tname, data,
                    context_instance=RequestContext(request))
        except TemplateDoesNotExist:
            return render_to_response('eagsite/page.html', data,
                    context_instance=RequestContext(request))
        return None

    def get_link_target(self):
        return None

    def get_absolute_url(self):
        return reverse('eagadmin.views.site', args=[self.slug])

    @property
    def next(self):
        return get_next(self)

    @property
    def prev(self):
        return get_prev(self)

    @property
    def children(self):
        return get_children(self)

    def __eq__(self, other):
        return self.slug == getattr(other, 'slug', None)

    def __str__(self):
        return "%s %s" % ("--" * self.level, self.title)

