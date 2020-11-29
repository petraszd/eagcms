from eagadmin.models.pages import Page
from eagadmin.types import register
from eagadmin.forms import PicasaWidget, WYSIWYGWidget, SemiWYSIWYGWidget
from google.appengine.ext import db
from django.http import HttpResponseRedirect
from django import forms

class Menu(Page):
    pass

class Text(Page):
    content = db.TextProperty(required=False)

# Should be forms.Form subclass
class TextForm(forms.Form):
    content = forms.CharField(widget=SemiWYSIWYGWidget)

    # If you want to turn on WYSIWYG editor on page load
    #content = forms.CharField(widget=WYSIWYGWidget)

class Link(Page):
    url = db.StringProperty()
    target = db.StringProperty(choices=['_self', '_blank'])

    # This is used by eagsite eagsite_list_menu template tag
    # to get link's target (_blank, _self)
    def get_link_target(self):
        return self.target

    # Response is redirect just in case some literally enters
    # this page's url
    def get_response(self, request):
        return HttpResponseRedirect(self.url)

    # Django's way
    def get_absolute_url(self):
        return self.url

register.add(Text, TextForm)
register.add(Link)
register.add(Menu)

