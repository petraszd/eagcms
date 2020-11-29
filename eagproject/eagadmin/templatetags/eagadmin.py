from django import template
from django.template.defaultfilters import stringfilter
from google.appengine.api import users
from django.core.urlresolvers import reverse

register = template.Library()

@register.filter
def margin_left(value):
    return "margin-left: %dem;" % (int(value - 1) * 3)

class LoginedUserNode(template.Node):
    def render(self, context):
        html = '<a class="logout" href="%s">Logout</a>%s&nbsp;'
        username = users.get_current_user().nickname()
        url = users.create_logout_url(reverse("eagadmin:index"))
        return html % (url, username)

def logout(parser, token):
    return LoginedUserNode()
register.tag('logout', logout)

