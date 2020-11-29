.. _tutorial:

********
Tutorial
********

.. _tut-intro:

Intro
=====

EAG cms is as simple as possible CMS for Google App Engine (GAE) and Django

EAG cms is made using these technologies: Google App Engine and Django. So, I
highly recommend You to read their documentation (and tutorials) first:

`Google App Engine Docs <http://code.google.com/appengine/docs/python/overview.html>`_

`Django Docs <http://docs.djangoproject.com/en/1.1/>`_

.. _tut-installing:

Getting started
===============

EAG cms completely depends from GAE. So, only way to publish something created
with it is through GAE. This means that You will be creating GAE application -
nothing less, nothing more.

Now we do not need to publish (And You can find that topic in GAE
documentation) - we need to test something in localhost. At least I am
thinking You want to do that...

Prepare dev environment
-----------------------

All commands are tested in Linux OS only. I am sorry, but I can not make
instructions for Windows and/or Mac OS users - I do not have these OS's.
On the other hand, these OS's have GUI tools. So, use my instruction, these
tools and common sense and I think You will do just fine.

Download GAE SDK, unzip it and enter newly created directory.::

   wget http://googleappengine.googlecode.com/files/google_appengine_<last-version>.zip
   unzip google_appengine_<last-version>.zip
   cd google_appengine/

You can skip Django installation step if You have installed it already. But
(It is important!!!) You need 1.1.* Django's version.

Download Django 1.1.*, untar it and make it local library for GAE SDK.::

   wget http://media.djangoproject.com/releases/1.1.2/Django-1.1.2.tar.gz
   tar zxf Django-1.1.2.tar.gz
   mv Django-1.1.2/django/ ./
   rm -r Django-1.1.2

Download EAG cms, untar it into projects/eagcms directory.::

   mkdir -p projects
   wget http://cdn.bitbucket.org/petraszd/eagcms/downloads/eagcms-0.1.2.tar.gz
   tar zxf eagcms-0.1.2.tar.gz
   mv eagcms projects

Rename main.py.sample into main.py
Rename eagproject/settings.py.sample into eagproject/settings.py::

   mv projects/eagcms/main.py.sample projects/eagcms/main.py
   mv projects/eagcms/eagproject/settings.py.sample projects/eagcms/eagproject/settings.py

Run dev environment::

  ./dev_appserver.py projects/eagcms

Default url of backend is `http://localhost:8080/admin/ <http://localhost:8080/admin/>`_.

Frontend: `http://localhost:8080/ <http://localhost:8080/>`_.

`More about dev environment <http://code.google.com/appengine/docs/python/gettingstarted/devenvironment.html>`_.


.. _tut-admin-interface:

Admin Interface
===============

.. image:: http://lh5.ggpht.com/_THWKK-dlQng/S3c0vDDlSAI/AAAAAAAAAOk/XCAMtnXCqGg/s800/index-hl.png

1. Add new page to site tree
2. To reorder site tree
3. Page's title
4. Page's type
5. Page's controls


.. _tut-simple-web-site:

Simple web site
===============

Creating
--------

Go to `http://localhost:8080/ <http://localhost:8080/>`_.

.. image:: http://lh6.ggpht.com/_THWKK-dlQng/S3iJEu8fYaI/AAAAAAAAAPY/FqjZHC2e6mw/s800/site-start.png

Your site is empty. Go to `http://localhost:8080/admin/ <http://localhost:8080/admin/>`_.
and add three pages:

* 'Main Menu' with
  top = 'Home Page', title = 'Main Menu', slug = 'main-menu', type = 'Menu'
* 'Foo' with
  top = 'Main Menu', title = 'Foo', slug = 'foo', type = 'Text'
* 'Bar' with
  top = 'Main Menu', title = 'Bar', slug = 'bar', type = 'Text'

.. image:: http://lh3.ggpht.com/_THWKK-dlQng/S3iJEptU5gI/AAAAAAAAAPc/TJl8oL7IT7s/s800/admin-after-menu.png

Now Your site has a menu

.. image:: http://lh3.ggpht.com/_THWKK-dlQng/S3iJEjac3jI/AAAAAAAAAPg/zccCC4FxxeE/s800/site-with-menu.png


Edit
----

In admin, edit page 'Foo'. When editing You can see more fields than You were
able when You were creating that page. It is because now page has type (Text)
and nows that text can have 'content'.

Enter some stupid (Example: 'foo foo foo') text to Foo's content.

.. image:: http://lh3.ggpht.com/_THWKK-dlQng/S3iJE2lLoVI/AAAAAAAAAPk/94_ELEGVTnw/s800/edit-content.png


Types' templates
----------------

Each page' type may have it's own template, which is rendered when you enter
that page in frontend.

Just take a look at 'templates/eagsite/'::

   tree templates/eagsite/

   # templates/eagsite/
   # |-- base.html
   # |-- page.html
   # `-- types
   #     `-- text.html

.. highlight:: django

This is templates where You can (and You should) customize Your site's look
and feel. 'types' are folder where You can put custom types' templates. Take a
look at text.html::

   {% extends "eagsite/page.html" %}
   {% block custom %}
   <div class="text">{{ current.content|safe }}</div>
   {% endblock %}

It simple extends page.html template and outputs page's content var.
Each type may have template. If now template is pressed than system falls back
to page.html template. So, that one must be presented.

'Home' type
-----------

Now You are going to create Your own page type - 'Home' type.

Take a look at 'base.html'::

   {% eagsite_get_page "" as root %}
   <div id="Wrapper">
       {# ... #}
       <h1 id="SiteName">&lt;Site Name&gt;</h1>
   </div>
   <div id="Footer">
     Copyright (c) &lt;Year&gt; &lt;Name Surname|Company's Name&gt;
   </div>

You probably can replace 'Site Name' and copyright by hand in template
because there is almost zero change they are going to change. But now We are
learning stuff and You are going to learn how to make these fields changeable
via root page ('Home Page').

.. highlight:: python

Go into 'eagproject/eagtypes.py', add and register 'Home' class::

   class Home(Page):
       footer = db.StringProperty(required=False)

   register.add(Home)

Now go to admin and change 'Home Page' type to 'Home'. Edit 'Home Page' and
change title to 'My Site' and footer to 'Copyright by Me'.

We are going to use it's title as site's name and footer as footer.

.. highlight:: django

Go to 'base.html' and change::

   <h1 id="SiteName">&lt;Site Name&gt;</h1> --> <h1 id="SiteName">{{ root.title }}</h1>

And::

   Copyright (c) &lt;Year&gt; &lt;Name Surname|Company's Name&gt; --> {{ root.footer }}

Result:

.. image:: http://lh6.ggpht.com/_THWKK-dlQng/S3iJFIxJ8UI/AAAAAAAAAPo/i2OaR0e34MQ/s800/site-double-header.png

Ok, that double mention of 'My site' is a little bit annoying. So, let's
change it.

Create 'templates/eagsite/types/home.html'::

   {% extends "eagsite/base.html" %}
   {% block content %}
   <h1 style="text-align: center;">Welcome!!!</h1>
   {% endblock %}

.. image:: http://lh6.ggpht.com/_THWKK-dlQng/S3iJ4hzPQRI/AAAAAAAAAPw/5WNcDiTP1GI/s800/site-finish.png

That's better.


.. _tut-eagtypes-concept:

EAG Types concept
=================

Site tree consist of :ref:`Page <class-page>` objects (direct or
subclasses). Page is subclass of GAE PolyModel class. So all Page's subclasses
are PolyModels too. Each Page object has `top` and `order` params - these two
are enough to calculate order of each node in site tree.

.. highlight:: python

Page class specifies some common attributes (:ref:`more details <class-page>`), but
"real" data attributes must be specified by project. This is done by using
EAGCMS_TYPES settings option and :ref:`register <object-register>` object::

   # settings.py:
   EAGCMS_TYPES = ('eagtypes',)

   # eagtypes.py:
   from eagadmin.types import register
   from google.appengine.ext import db
   from eagadmin.forms import SemiWYSIWYGWidget
   from django.http import HttpResponseRedirect
   from django import forms

   class Text(Page):
       content = db.TextProperty(required=False)

   class TextForm(forms.Form):
       content = forms.CharField(widget=SemiWYSIWYGWidget)

   class Link(Page):
       url = db.StringProperty()
       target = db.StringProperty(choices=['_self', '_blank'])

       def get_link_target(self):
           return self.target

       def get_response(self, request):
           return HttpResponseRedirect(self.url)

       def get_absolute_url(self):
           return self.url

   register.add(Text, TextForm)
   register.add(Link)

This code sample registers two page types: *Text* and *Link*.

First: Text classes objects will have content field. Default TextProperty's
fields objects are rendering using simple textarea. If You do not want that and
want to have WYSIWYG editor to enter HTML content You can create
django.forms.Form subclass, make *content* field's widget as SemiWYSIWYGWidget
(or WYSIWYGWidget) and pass it as second param to registers.add method.

Second: Link. It is more interesting class because it shows some inner stuff
EAG cms does to render pages.

*get_link_target* method returns self.target, which can be '_self' or '_blank'.
Page's implementation returns '_blank'. This method is used for rendering
site's menu(s).

*get_absolute_url* is standard django's way of returning models' urls. The only
different - it is not django's ORM model, it is GAE model object.

*get_response*. It is really interesting method, because this method is
responsible for returning response of a Page. So if You enter page's url page
itself renders content. It is small violation of MVC pattern, but it lets you
to define interesting Page types (Link for example).

Section below talks about real Page's *get_response* implementation.


.. _tut-look-and-feel:

Customizing look and feel
=========================

So, if you do not change Page's subclasses default *get_response*
implementation, each page would be rendered using this algorithm:

* Template var *current* is set to current page
* Template var *breadcrumb* is set to list of page's breadcrumb
* Template 'eagsite/types/<class-name-lowercase.html is rendered using
  those vars
* If such template does not exists - template 'eagsite/page.html' is rendered

So site at least must have 'eagsite/page.html' template. It simple django
template - you must edit it (and/or 'eagsite/types/\*.html') to change Yours
applications look and feel.


.. _tut-app-integration:

Fictional Django app integration (Advanced topic)
=================================================

.. highlight:: python

I am goning to show You how to integrate Django application into EAG cms. It
is advanced part of tutorial - so, I am going to rush through code without a
lot of explanation.

Lets start by creating application nothing (We are in 'eagproject' dir)::

   mkdir nothing
   touch nothing/__init__.py
   touch nothing/views.py
   touch nothing/urls.py

nothing/views.py::

   from django.template import RequestContext
   from django.shortcuts import render_to_response
   from eagadmin.account import admin_required

   @admin_required
   def admin(request):
       return render_to_response('nothing/admin.html', {},
               context_instance=RequestContext(request))

   def site(request):
       return render_to_response('nothing/site.html', {},
               context_instance=RequestContext(request))

nothing/urls.py::

   from django.conf.urls.defaults import *

   urlpatterns = patterns('nothing.views',
           url(r'^admin/$', 'admin', name='admin'),
           url(r'^.*$', 'site', name='site'),
   )


Edit settings.py by adding nothing to applications list::

   EAGCMS_TYPES = (
       'eagtypes',
       'nothing',
   )

Edit urls.py::

   from django.conf.urls.defaults import *
   urlpatterns = patterns('',
       (r'^nothing/', include('nothing.urls', namespace='nothing')),
       # Rest of file ...

Prepare existing templates for nothing integration.

.. highlight:: django

templates/eagsite/base.html::

   {# ... #}
   <ul id="Menu">
     <li class="home {% ifequal current root %}current{% endifequal %}"><a href="{{ root.get_absolute_url }}">{{ root.menu_title}} </a>
     {% eagsite_list_menu "main-menu" %}
     <li class="{% block nothing_menu %}{% endblock %}" ><a href="{% url nothing:site %}">Nothing</a>
   </ul>
   {# ... #}

templates/eagadmin/base.html::

   <ul id="TopMenu">
     <li class="{% block menu_sitetree %}{% endblock %}">
       <a href="{% url eagadmin:index %}">{% trans "Site Tree" %}</a>
     </li>
     <li class="{% block menu_nothing %}{% endblock %}">
       <a href="{% url nothing:admin %}">{% trans "Nothing" %}</a>
     </li>
   </ul>

Now You can create templates for Your new django's application::

   mkdir templates/nothing
   touch templates/nothing/site.html
   touch templates/nothing/admin.html

templates/nothing/site.html::

   {% extends "eagsite/base.html" %}
   {% block nothing_menu %}current{% endblock %}
   {% block content %}
   Nothing here...
   {% endblock %}

templates/nothing/admin.html::

   {% extends "eagadmin/base.html" %}
   {% block menu_nothing %}active{% endblock %}
   {% block content %}Nothing here...{% endblock %}

And finnaly You have application 'nothing' who does nothing:

.. image:: http://lh5.ggpht.com/_THWKK-dlQng/S3iJ4l7yuBI/AAAAAAAAAP0/EJfT-MGZi4I/s800/site-nothing.png

.. image:: http://lh3.ggpht.com/_THWKK-dlQng/S3iJ4w63SbI/AAAAAAAAAP4/ImSp_FfLAI4/s800/admin-nothing.png

