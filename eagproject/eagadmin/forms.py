from google.appengine.ext.db import djangoforms
from eagadmin.models.pages import Page, get_all, choices
from django.utils.importlib import import_module
from django import forms
from eagadmin.types import get_namepairs

def form_formclass(class_, additional=None):
    class ContentForm(djangoforms.ModelForm):
        def __init__(self, *args, **kwargs):
            super(ContentForm, self).__init__(*args, **kwargs)
            if not additional:
                return
            for k, field in additional.base_fields.iteritems():
                self.fields[k] = field
        class Meta:
            model = class_
            exclude = Page.properties().keys()
    return ContentForm

class TypeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(TypeForm, self).__init__(*args, **kwargs)

        self.fields['type'] = djangoforms.forms.ChoiceField(
                choices=get_namepairs())

class PageForm(djangoforms.ModelForm):
    class Meta:
        model = Page
        exclude = ('order', 'level', 'updated_by', '_class',)

    def __init__(self, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)

        ChoiceField= djangoforms.forms.ChoiceField
        if self.instance and self.instance.is_saved():
            del(self.fields['top'])
        else:
            self.fields['top'] = ChoiceField(choices=choices(), widget=djangoforms.forms.Select)
            self.fields['type'] = ChoiceField(choices=get_namepairs())

class PicasaWidget(forms.TextInput):
    def __init__(self, *args, **kwargs):
        super(PicasaWidget, self).__init__(*args, **kwargs)
        self.attrs['class'] = 'picasa'

class WYSIWYGWidget(forms.Textarea):
    def __init__(self, *args, **kwargs):
        super(WYSIWYGWidget, self).__init__(*args, **kwargs)
        self.attrs['class'] = 'wysiwyg'

class SemiWYSIWYGWidget(forms.Textarea):
    def __init__(self, *args, **kwargs):
        super(SemiWYSIWYGWidget, self).__init__(*args, **kwargs)
        self.attrs['class'] = 'semi-wysiwyg'

