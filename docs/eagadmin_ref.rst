.. _eagadmin-ref:


*******************************
eagadmin django app's reference
*******************************

:mod:`eagadmin.models.pages` --- EAG cms admin models
=====================================================

.. module:: eagadmin.models.pages
.. currentmodule:: eagadmin.models.pages

.. function:: get_root()

   Returns root page


.. function:: choices()

   Generator. Generates ``(page.key, str(page))`` pairs for all pages.


.. function:: get_all()

   Returns list of all pages


.. function:: get_branch(page)

   Returns *page*'s branch. Passed *page* is not included in result.


.. function:: get_children(page)

   Returns *page*'s children with correct order


.. function:: get_prev(page)

   Returns *page*'s previous sibling.


.. function:: get_next(page)

   Returns *page*'s next sibling.


.. function:: get_by_slug([slug=''])

   Returns:

   - root if not slug
   - First *Page* object with slug equals *slug*
   - None if such *Page* object does not exists


.. function:: get_descendants(page[, depth=-1])

   Returns list of *page*'s descendants. Param *depth* tells how deep go into
   a tree. if *depth* equals -1 returns all descendants. Passed page is not
   included in result.


.. function:: get_breadcrumb(page)

   Returns breadcrumb from root to *page*. Passed *page* is included in result
   as last elem.


.. function:: add_as_last_child(page, destination)


.. function:: add_root()

   Creates root page. ``get_root`` calls it when there is no root present.
   Returns created Page object.


.. function:: delete_with_branch(page)

   Deletes *page* and all it's descendants.


.. function:: reorder(neworder)

   *neworder* must be a list of pairs (page's key, page's new level)


.. function:: to_type(page, newtype)

   Returns new page with class *newtype* having same fields as passed page.
   *newtype* must be string and can not be class object.


.. function:: reparent(old_parent, new_parent)

   Sets *new_parent* as *top* attribute to all *old_parent*'s children.


:class:`eagadmin.models.pages.Page` --- Page class
--------------------------------------------------

.. _class-page:

.. class:: Page

   `google.appengine.ext.db.polymodel.PolyModel <http://code.google.com/appengine/docs/python/datastore/polymodelclass.html>`_ sublcass.


.. attribute:: Page.top

   Page's parent. *parent* is reserved by Google App Engine, so *top* has
   been chosen.

   *children_set* does not guarantee to return them in correct order. Use
   **Page.children** or **pages.get_children** instead.

   ``google.appengine.ext.db.SelfReferenceProperty(collection_name='children_set')``


.. attribute:: Page.order

   ``google.appengine.ext.db.IntegerProperty(required=True, default=0)``


.. attribute:: Page.level

   Page's level. Must contain correct level. Starts from zero (Root has zero).

   ``google.appengine.ext.db.IntegerProperty(required=True, default=0)``


.. attribute:: Page.title

   ``google.appengine.ext.db.StringProperty(required=True)``


.. attribute:: Page.slug

   ``google.appengine.ext.db.StringProperty(required=True)``


.. attribute:: Page.menu_name

   Page's name that is showed in menus.

   ``google.appengine.ext.db.StringProperty()``


.. attribute:: Page.draft

   Page is not reachable if it has draft=True

   ``google.appengine.ext.db.BooleanProperty()``


.. attribute:: Page.keywords

   ``google.appengine.ext.db.TextProperty()``


.. attribute:: Page.description

   ``google.appengine.ext.db.TextProperty()``


.. attribute:: Page.updated_at

   ``google.appengine.ext.db.DateTimeProperty(auto_now=True)``


.. attribute:: Page.updated_by

   ``google.appengine.ext.db.UserProperty(auto_current_user=True)``

.. attribute:: Page.menu_title

   Returns *menu_name*. If it is empty, than returns *title*. This is a
   read-only attribute.

.. attribute:: Page.next()

   Next sibling. This is a read-only attribute.

.. attribute:: Page.prev()

   Previous sibling. This is a read-only attribute.

.. attribute:: Page.children()

   Page's children in correct order. This is a read-only attribute.

.. method:: Page.is_root()

   If page is a root.

.. method:: Page.is_leaf()

   If page is a leaf.

.. method:: Page.has_top()

   If page has a top (parent).

.. method:: Page.has_children()

.. method:: Page.has_next()

.. method:: Page.has_prev()

.. method:: Page.get_response(request)

   Method gets Django's request object and must return Django's response
   object.

   Page's implementation tries to render
   *eagsite/types/<class_name_lower>.html template*. It it is not present -
   falls back to *eagsite/page.html*.

   Template is rendered with these variables::

      data = {
          'current': self,
          'breadcrumb': get_breadcrumb(self)
      }

.. method:: Page.get_link_target(self)

   Returns link target used for menu rendering. ``<a href="" target="<target>">menu_title </a>``

.. method:: Page.get_absolute_url(self)

   Django's kind of way to get link for eagsite.


:mod:`eagadmin.forms` --- EAG cms admin forms
=============================================

.. module:: eagadmin.forms
.. currentmodule:: eagadmin.forms


.. _class-picasa-widget:

.. class:: PicasaWidget

   Lets select picasaweb galleries image.

   ::

      field_name = forms.CharField(widget=PicasaWidget)

.. class:: WYSIWYGWidget

   `Mooeditable <http://cheeaun.github.com/mooeditable/>`_ widget.

   ::

      field_name = forms.CharField(widget=WYSIWYGWidget)

.. class:: SemiWYSIWYGWidget

   Textarea with possibility to turn it in WYSIWYG Editor.


:mod:`eagadmin.types` --- EAG cms admin types
=============================================

.. module:: eagadmin.types
.. currentmodule:: eagadmin.types

.. _object-register:

.. data:: register

   Global Register object you should use to register new site tree's page types::

      from eagadmin.models.pages import Page
      from eagadmin.types import register
      from django import forms

      class NewType(Page):
          pass # Custom attributes

      class NewTypeForm(forms.Form):
          pass # Custom fields for some or all custom attributes

      register.add(Text, TextForm)

.. class:: Register

.. attribute:: Register.types

   Returns all registered types.

.. method:: Register.add(modelcl=None, formcl=None)

   Adds new type to possible site tree's node classes.
   *modelcl* must be **eagadmin.models.page.Page** subclass.
   *formcl* must be django.forms subclass. There is no effect of using django
   models or gae models forms, because eagadmin uses just field definition, not
   class itself.

.. class:: PageType

   Helper class for Register.

.. attribute:: Page.modelcl
.. attribute:: Page.formcl

