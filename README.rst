Introduction
============

Change some parts of Plone and make possible for users to delete contents not so easily.

The Plone behaviour
-------------------

Plone (Zope) base the power to delete object looking for the "*Delete objects*" permission on *containers*.
This mean that normally users that can delete contents inside a folder can delete **all** contents.
In our experience, no-one want a workflow that make possibile to users that can't modify a content, to be able to delete it.

This product change the Plone user interface behaviour, hiding the possibility to delete contents when you can't modify it.

How Plone works after the installation
--------------------------------------

For deleting a content you must have:

* "*Delete objects*" permission on the parent folder
* "*Delete objects*" permission on the content itself
* Beeing able to modify the content (*all* the contents) you want to delete

Security
--------

This product is targeted on Plone UI. If you run a task, a 3rd party product or whatever piece of code that delete objects,
this will run with the default Plone permissions (so, only checking the "*Delete objects*" on containers.

Requirements
============

This product has been tested and used on Plone. 

Authors
=======

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.net/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.net/

