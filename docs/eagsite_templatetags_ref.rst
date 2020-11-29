.. _eagsite_templatetags_ref:


*******************************
eagsite template tags reference
*******************************

:mod:`eagadmin.templatetags.eagsite` --- EAG cms frontend template tags
=======================================================================

.. highlight:: django

.. describe:: eagsite_list_menu

   ::

      {% eagsite_head %}

      Outputs:

      <title>{{ current.title }}</title>
      <meta name="keywords" content="{{ current.keywords }}">
      <meta name="description" content="{{ current.description }}" >


.. describe:: eagsite_get_page

   ::

      {% eagsite_get_page "some-slug" as some_page %}

   Add Page object with slug "some-slug" as template var *some_page*.


.. describe:: eagsite_head

   ::

      {% eagsite_list_menu "main-menu" %}
      <ul id="Menu">
        {% eagsite_list_menu "some-slug" depth %}
      </ul>

   Renders menu with page's (with slug "some-slug") descendants and with depth *depth*.

   Slug is optional (root is used instead). *depth* is optional (1 is used instead).

   Generated lis can have these classes:

   - <li class="first"> if it is first li
   - <li class="current"> if current.slug == menu_item.slug
   - <li class="branch"> if current page is descendant of menu_item

