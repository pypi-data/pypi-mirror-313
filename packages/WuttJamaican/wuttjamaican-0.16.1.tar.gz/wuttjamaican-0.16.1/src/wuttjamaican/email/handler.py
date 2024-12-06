# -*- coding: utf-8; -*-
################################################################################
#
#  WuttJamaican -- Base package for Wutta Framework
#  Copyright © 2023-2024 Lance Edgar
#
#  This file is part of Wutta Framework.
#
#  Wutta Framework is free software: you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option) any
#  later version.
#
#  Wutta Framework is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#
#  You should have received a copy of the GNU General Public License along with
#  Wutta Framework.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Email Handler
"""

import logging
import smtplib

from wuttjamaican.app import GenericHandler
from wuttjamaican.util import resource_path
from wuttjamaican.email.message import Message


log = logging.getLogger(__name__)


class EmailHandler(GenericHandler):
    """
    Base class and default implementation for the :term:`email
    handler`.

    Responsible for sending email messages on behalf of the
    :term:`app`.

    You normally would not create this directly, but instead call
    :meth:`~wuttjamaican.app.AppHandler.get_email_handler()` on your
    :term:`app handler`.
    """

    # nb. this is fallback/default subject for auto-message
    universal_subject = "Automated message"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        from mako.lookup import TemplateLookup

        # prefer configured list of template lookup paths, if set
        templates = self.config.get_list(f'{self.config.appname}.email.templates')
        if not templates:

            # otherwise use all available paths, from app providers
            available = []
            for provider in self.app.providers.values():
                if hasattr(provider, 'email_templates'):
                    templates = provider.email_templates
                    if isinstance(templates, str):
                        templates = [templates]
                    if templates:
                        available.extend(templates)
            templates = available

        # convert all to true file paths
        if templates:
            templates = [resource_path(p) for p in templates]

        # will use these lookups from now on
        self.txt_templates = TemplateLookup(directories=templates)
        self.html_templates = TemplateLookup(directories=templates,
                                             # nb. escape HTML special chars
                                             # TODO: sounds great but i forget why?
                                             default_filters=['h'])

    def make_message(self, **kwargs):
        """
        Make and return a new email message.

        This is the "raw" factory which is simply a wrapper around the
        class constructor.  See also :meth:`make_auto_message()`.

        :returns: :class:`~wuttjamaican.email.message.Message` object.
        """
        return Message(**kwargs)

    def make_auto_message(self, key, context={}, **kwargs):
        """
        Make a new email message using config to determine its
        properties, and auto-generating body from a template.

        Once everything has been collected/prepared,
        :meth:`make_message()` is called to create the final message,
        and that is returned.

        :param key: Unique key for this particular "type" of message.
           This key is used as a prefix for all config settings and
           template names pertinent to the message.

        :param context: Context dict used to render template(s) for
           the message.

        :param \**kwargs: Any remaining kwargs are passed as-is to
           :meth:`make_message()`.  More on this below.

        :returns: :class:`~wuttjamaican.email.message.Message` object.

        This method may invoke some others, to gather the message
        attributes.  Each will check config, or render a template, or
        both.  However if a particular attribute is provided by the
        caller, the corresponding "auto" method is skipped.

        * :meth:`get_auto_sender()`
        * :meth:`get_auto_subject()`
        * :meth:`get_auto_to()`
        * :meth:`get_auto_cc()`
        * :meth:`get_auto_bcc()`
        * :meth:`get_auto_txt_body()`
        * :meth:`get_auto_html_body()`
        """
        kwargs['key'] = key
        if 'sender' not in kwargs:
            kwargs['sender'] = self.get_auto_sender(key)
        if 'subject' not in kwargs:
            kwargs['subject'] = self.get_auto_subject(key, context)
        if 'to' not in kwargs:
            kwargs['to'] = self.get_auto_to(key)
        if 'cc' not in kwargs:
            kwargs['cc'] = self.get_auto_cc(key)
        if 'bcc' not in kwargs:
            kwargs['bcc'] = self.get_auto_bcc(key)
        if 'txt_body' not in kwargs:
            kwargs['txt_body'] = self.get_auto_txt_body(key, context)
        if 'html_body' not in kwargs:
            kwargs['html_body'] = self.get_auto_html_body(key, context)
        return self.make_message(**kwargs)

    def get_auto_sender(self, key):
        """
        Returns automatic
        :attr:`~wuttjamaican.email.message.Message.sender` address for
        a message, as determined by config.
        """
        # prefer configured sender specific to key
        sender = self.config.get(f'{self.config.appname}.email.{key}.sender')
        if sender:
            return sender

        # fall back to global default (required!)
        return self.config.require(f'{self.config.appname}.email.default.sender')

    def get_auto_subject(self, key, context={}, rendered=True):
        """
        Returns automatic
        :attr:`~wuttjamaican.email.message.Message.subject` line for a
        message, as determined by config.

        This calls :meth:`get_auto_subject_template()` and then
        renders the result using the given context.

        :param rendered: If this is ``False``, the "raw" subject
           template will be returned, instead of the final/rendered
           subject text.
        """
        from mako.template import Template

        template = self.get_auto_subject_template(key)
        if not rendered:
            return template
        return Template(template).render(**context)

    def get_auto_subject_template(self, key):
        """
        Returns the template string to use for automatic subject line
        of a message, as determined by config.

        In many cases this will be a simple string and not a
        "template" per se; however it is still treated as a template.

        The template returned from this method is used to render the
        final subject line in :meth:`get_auto_subject()`.
        """
        # prefer configured subject specific to key
        template = self.config.get(f'{self.config.appname}.email.{key}.subject')
        if template:
            return template

        # fall back to global default
        return self.config.get(f'{self.config.appname}.email.default.subject',
                               default=self.universal_subject)

    def get_auto_to(self, key):
        """
        Returns automatic
        :attr:`~wuttjamaican.email.message.Message.to` recipient
        address(es) for a message, as determined by config.
        """
        return self.get_auto_recips(key, 'to')

    def get_auto_cc(self, key):
        """
        Returns automatic
        :attr:`~wuttjamaican.email.message.Message.cc` recipient
        address(es) for a message, as determined by config.
        """
        return self.get_auto_recips(key, 'cc')

    def get_auto_bcc(self, key):
        """
        Returns automatic
        :attr:`~wuttjamaican.email.message.Message.bcc` recipient
        address(es) for a message, as determined by config.
        """
        return self.get_auto_recips(key, 'bcc')

    def get_auto_recips(self, key, typ):
        """ """
        typ = typ.lower()
        if typ not in ('to', 'cc', 'bcc'):
            raise ValueError("requested type not supported")

        # prefer configured recips specific to key
        recips = self.config.get_list(f'{self.config.appname}.email.{key}.{typ}')
        if recips:
            return recips

        # fall back to global default
        return self.config.get_list(f'{self.config.appname}.email.default.{typ}',
                                    default=[])

    def get_auto_txt_body(self, key, context={}):
        """
        Returns automatic
        :attr:`~wuttjamaican.email.message.Message.txt_body` content
        for a message, as determined by config.  This renders a
        template with the given context.
        """
        template = self.get_auto_body_template(key, 'txt')
        if template:
            return template.render(**context)

    def get_auto_html_body(self, key, context={}):
        """
        Returns automatic
        :attr:`~wuttjamaican.email.message.Message.html_body` content
        for a message, as determined by config.  This renders a
        template with the given context.
        """
        template = self.get_auto_body_template(key, 'html')
        if template:
            return template.render(**context)

    def get_auto_body_template(self, key, typ):
        """ """
        from mako.exceptions import TopLevelLookupException

        typ = typ.lower()
        if typ not in ('txt', 'html'):
            raise ValueError("requested type not supported")

        if typ == 'txt':
            templates = self.txt_templates
        elif typ == 'html':
            templates = self.html_templates

        try:
            return templates.get_template(f'{key}.{typ}.mako')
        except TopLevelLookupException:
            pass

    def deliver_message(self, message, sender=None, recips=None):
        """
        Deliver a message via SMTP smarthost.

        :param message: Either a
           :class:`~wuttjamaican.email.message.Message` object or
           similar, or a string representing the complete message to
           be sent as-is.

        :param sender: Optional sender address to use for delivery.
           If not specified, will be read from ``message``.

        :param recips: Optional recipient address(es) for delivery.
           If not specified, will be read from ``message``.

        A general rule here is that you can either provide a proper
        :class:`~wuttjamaican.email.message.Message` object, **or**
        you *must* provide ``sender`` and ``recips``.  The logic is
        not smart enough (yet?) to parse sender/recips from a simple
        string message.

        Note also, this method does not (yet?) have robust error
        handling, so if an error occurs with the SMTP session, it will
        simply raise to caller.

        :returns: ``None``
        """
        if not sender:
            sender = message.sender
            if not sender:
                raise ValueError("no sender identified for message delivery")

        if not recips:
            recips = set()
            if message.to:
                recips.update(message.to)
            if message.cc:
                recips.update(message.cc)
            if message.bcc:
                recips.update(message.bcc)
        elif isinstance(recips, str):
            recips = [recips]

        recips = set(recips)
        if not recips:
            raise ValueError("no recipients identified for message delivery")

        if not isinstance(message, str):
            message = message.as_string()

        # get smtp info
        server = self.config.get(f'{self.config.appname}.mail.smtp.server', default='localhost')
        username = self.config.get(f'{self.config.appname}.mail.smtp.username')
        password = self.config.get(f'{self.config.appname}.mail.smtp.password')

        # make sure sending is enabled
        log.debug("sending email from %s; to %s", sender, recips)
        if not self.sending_is_enabled():
            log.debug("nevermind, config says no emails")
            return

        # smtp connect
        session = smtplib.SMTP(server)
        if username and password:
            session.login(username, password)

        # smtp send
        session.sendmail(sender, recips, message)
        session.quit()
        log.debug("email was sent")

    def sending_is_enabled(self):
        """
        Returns boolean indicating if email sending is enabled.

        Set this flag in config like this:

        .. code-block:: ini

           [wutta.mail]
           send_emails = true

        Note that it is OFF by default.
        """
        return self.config.get_bool(f'{self.config.appname}.mail.send_emails',
                                    default=False)

    def send_email(self, key=None, context={}, message=None, sender=None, recips=None, **kwargs):
        """
        Send an email message.

        This method can send a ``message`` you provide, or it can
        construct one automatically from key/config/templates.

        :param key: Indicates which "type" of automatic email to send.
           Used to lookup config settings and template files.

        :param context: Context dict for rendering automatic email
           template(s).

        :param message: Optional pre-built message instance, to send
           as-is.

        :param sender: Optional sender address for the
           message/delivery.

           If ``message`` is not provided, then the ``sender`` (if
           provided) will also be used when constructing the
           auto-message (i.e. to set the ``From:`` header).

           In any case if ``sender`` is provided, it will be used for
           the actual SMTP delivery.

        :param recips: Optional list of recipient addresses for
           delivery.  If not specified, will be read from the message
           itself (after auto-generating it, if applicable).

           .. note::

              This param does not affect an auto-generated message; it
              is used for delivery only.  As such it must contain
              *all* true recipients.

              If you provide the ``message`` but not the ``recips``,
              the latter will be read from message headers: ``To:``,
              ``Cc:`` and ``Bcc:``

              If you want an auto-generated message but also want to
              override various recipient headers, then you must
              provide those explicitly::

                 context = {'data': [1, 2, 3]}
                 app.send_email('foo', context, to='me@example.com', cc='bobby@example.com')

        :param \**kwargs: Any remaining kwargs are passed along to
           :meth:`make_auto_message()`.  So, not used if you provide
           the ``message``.
        """
        if message is None:
            if sender:
                kwargs['sender'] = sender
            message = self.make_auto_message(key, context, **kwargs)

        self.deliver_message(message, recips=recips)
