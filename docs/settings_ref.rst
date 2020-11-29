.. _settings:

********
Settings
********


.. _settings-django:

Django setting.py variables
===========================

EAG cms needs You to define some options in standard Django's settings module.

ADMINS
------

Actually it is Django's standard settings' variable, but in EAG cms it is used
to define additional users that are allowed to edit content.

All users that are assigned as Yours app's administrators in appspots are
allowed to edit content anyway - so You do not need to add them to `ADMINS`
settings' var::

   ADMINS = (
       ('Default', 'test@example.com'),
   )

EAGCMS_TYPES
------------
modules list where EAG page types are defined.::

   EAGCMS_TYPES = (
       'eagtypes',
   )

See see :ref:`tut-eagtypes-concept` to find out more about page types.

EAGCMS_PICASA_USER
------------------

Optional. `Picasa Web <http://picasaweb.google.com/>`_ user's name
which public galleries are used to retrieve images for EAG cms wysiwyg
and image widget (:ref:`PicasaWidget <class-page>`). If no name is defined
than current logged in user's name is used instead::

   EAGCMS_PICASA_USER = 'some-user-name'


