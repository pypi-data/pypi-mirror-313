==============
rer.newsletter
==============

|python| |version| |ci| |license| |number|

.. |python| image:: https://img.shields.io/pypi/pyversions/rer.newsletter.svg
  :target: https://pypi.python.org/pypi/rer.newsletter/

.. |version| image:: http://img.shields.io/pypi/v/rer.newsletter.svg
  :target: https://pypi.python.org/pypi/rer.newsletter

.. |number| image:: http://img.shields.io/pypi/dm/rer.newsletter.svg
  :target: https://pypi.python.org/pypi/rer.newsletter

.. |license| image:: http://img.shields.io/pypi/l/rer.newsletter.svg
  :target: https://pypi.python.org/pypi/rer.newsletter

.. |ci| image:: https://github.com/RegioneER/rer.newsletter/actions/workflows/tests.yml/badge.svg
  :target: https://github.com/RegioneER/rer.newsletter/actions


This product allows the complete management of a newsletter.

========
Features
========

New Content-type
----------------

- Channel

  * Totally customizable because it is possible to set a header, a footer and CSS styles. This fields allows to uniform template of email that will be sent from one channel.
  * content type that inherit from folder content.

- Message

  * content type that inherit from folder content.

Portlet and Tile
----------------

The product provide a portlet and a tile for user subscribe.

Form for user subscribe have an email field and is protected for spam with `collective.honeypot <https://github.com/plone/collective.honeypot>`__.


User Management
---------------

Allows complete management of user.

- Add user from admin setting
- Delete user from admin setting
- Import users directly from CSV file
- Export users directly to CSV file
- Delete a group of user directly from CSV file
- Subscribe users
- Unsubscribe users


=================
Advanced Features
=================


Customize how to send your newsletter
-------------------------------------

By default, this product send all the emails through the standard plone mailer.
The actual sending mechanism is handled by an adapter (a multi-adapter)::

  <adapter
    for="rer.newsletter.behaviors.ships.IShippableMarker
         zope.publisher.interfaces.browser.IBrowserRequest"
    provides=".base_adapter.IChannelSender"
    factory=".base_adapter.BaseAdapter"
  />


To change this default activity, you can create a new Plone add-on that
register a new adapter with a more specific layer (e.g. use the browser layer
of the new add-on) and override the ``sendMessage`` method as you wish.

`rer.newsletterplugin.flask <https://github.com/RegioneER/rer.newsletterplugin.flask>`__ is an example
of plugin with a custom sender. It uses an external Flask app to send emails.


Advanced security
-----------------

New permissions have been added for the management of the Newsletter:

- ``rer.newsletter: Add Channel``
- ``rer.newsletter: Add Message``
- ``rer.newsletter: Manage Newsletter``
- ``rer.newsletter: Send Newsletter``

This permission are assigned to Manager and Site Administrator. There is also
a new role, ``Gestore Newsletter``, which has permissions for all possible
operations on newsletter.


Bot protection
==============

This product use `collective.honeypot <https://pypi.org/project/collective.honeypot/>`__ to prevent bot submissions.

You just need to set two environment variables:

- *EXTRA_PROTECTED_ACTIONS customer-satisfaction-add*
- *HONEYPOT_FIELD xxx*

xxx should be a field name that bot should compile.

If you get hacked, you could simply change that variable.


Subscriptions cleanup
----------------------

There is a view (*@@delete_expired_users*) that delete all
users that not have confirmed subscription to a channel in time.

You can set subscription token validity from the product's control panel.

Inside the settings of the product there is a field that allows you to set
validity time of the channel subscription token.


============
Installation
============

Install rer.newsletter by adding it to your buildout::

    [buildout]

    ...

    eggs =
        rer.newsletter


and then running ``bin/buildout``

============
Dependencies
============

This product has been tested on Plone 6 with volto integration.

=======
Credits
=======

Developed with the support of `Regione Emilia Romagna <http://www.regione.emilia-romagna.it/>`_;

Regione Emilia Romagna supports the `PloneGov initiative <http://www.plonegov.it/>`_.


=======
Authors
=======

This product was developed by **RedTurtle Technology** team.

.. image:: https://avatars1.githubusercontent.com/u/1087171?s=100&v=4
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.it/
