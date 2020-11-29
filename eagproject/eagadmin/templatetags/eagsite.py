from django import template
from django.template import TemplateSyntaxError, VariableDoesNotExist
from ..eagadmin import types
# Need to call load because these tags can be used without using
# eagadmin.views module
types.load()
from ..eagadmin.models import pages

register = template.Library()

class ListMenuNode(template.Node):
    def __init__(self, item, depth):
        self.item = template.Variable(item)
        self.depth = int(depth)

    def render(self, context):
        current = None
        breadcrumb = []
        try:
            current = template.Variable('current').resolve(context)
            breadcrumb = template.Variable('breadcrumb').resolve(context)
        except VariableDoesNotExist:
            current = None
        items = []
        item = None
        try:
            item = self.item.resolve(context)
            items = pages.get_descendants(item, self.depth)
        except AttributeError:
            item = pages.get_by_slug(str(item))
            if not item:
                item = pages.get_root()
            items = pages.get_descendants(item, self.depth)
        if not items:
            return ''
        return self.output(items, current, breadcrumb)

    def output(self, items, current=None, breadcrumb=[]):
        first = items[0]
        level = first.level
        out = []
        for i, p in enumerate(items):
            if level < p.level:
                out.append('<ul>')
            if level > p.level:
                out.append('</ul>' * (level - p.level))

            cl = []
            if not i:
                cl.append('first')
            if current and p == current:
                cl.append('current')
            elif p in breadcrumb:
                cl.append('branch')

            if cl:
                out.append('<li class="%s">' % (' '.join(cl)))
            else:
                out.append('<li>')

            target = ''
            if p.get_link_target():
                target = ' target="%s"' % p.get_link_target()
            params = (p.get_absolute_url(), target, p.menu_title)
            out.append('<a href="%s"%s>%s</a>' % params)
            level = p.level
        out.append('</ul>' * (level - first.level))
        return ''.join(out)

def list_menu(parser, token):
    args = token.split_contents()
    if len(args) >= 3:
        tag_name, item, depth = args[0], args[1], args[2]
    elif len(args) == 2:
        tag_name, item = args[0], args[1]
        depth = 1
    else:
        item = '""' # makes ListMenuNode to believe is empty str
        depth = 1
    return ListMenuNode(item, depth)
register.tag('eagsite_list_menu', list_menu)

class GetPageNode(template.Node):
    def __init__(self, slug, var_name):
        self.slug = template.Variable(slug)
        self.var_name = var_name

    def render(self, context):
        slug = self.slug.resolve(context)
        context[self.var_name] = pages.get_by_slug(str(slug))
        return ''

def get_page(parser, token):
    args = token.split_contents()
    if len(args) != 4 and args[2] != 'as':
        raise TemplateSyntaxError("%r tag must be {% %s 'page-slug' as var_name %}" % \
                (args[0], args[0]))
    return GetPageNode(args[1], args[3])
register.tag('eagsite_get_page', get_page)

class HeadNode(template.Node):
    def render(self, context):
        try:
            current = template.Variable('current').resolve(context)
        except VariableDoesNotExist:
            return ''
        return '<title>%s</title>' \
            '<meta name="keywords" content="%s">' \
            '<meta name="description" content="%s" >' \
            % (current.title, current.keywords or '', current.description or '')

def head(parser, token):
    return HeadNode()
register.tag('eagsite_head', head)

