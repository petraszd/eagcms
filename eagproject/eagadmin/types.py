from django.conf import settings
from django.utils.datastructures import SortedDict
from django.forms import Form

def load():
    for modulepath in settings.EAGCMS_TYPES:
        module = __import__(modulepath, globals(), locals())

def get_namepairs():
    for name in register.types.keys():
        yield (name, name)

def get_formclass(page):
    # to prevent cross imports
    from eagadmin.forms import form_formclass
    cl = page.class_name()
    if not cl in register.types:
        return form_formclass(page.__class__)
    additional = register.types[cl].formcl
    return form_formclass(page.__class__, additional)

def get_types():
    return register.types

class PageType(object):
    def __init__(self, modelcl, formcl):
        self.modelcl = modelcl
        self.formcl = formcl

class Register(object):
    def __init__(self):
        self._types = SortedDict()

    @property
    def types(self):
        return self._types

    def add(self, modelcl=None, formcl=None):
        self._types[modelcl.__name__] = PageType(modelcl, formcl)

register = Register()

