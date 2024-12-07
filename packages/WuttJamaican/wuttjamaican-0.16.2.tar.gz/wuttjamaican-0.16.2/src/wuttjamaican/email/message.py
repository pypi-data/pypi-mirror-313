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
Email Message
"""

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Message:
    """
    Represents an email message to be sent.

    :param to: Recipient(s) for the message.  This may be either a
       string, or list of strings.  If a string, it will be converted
       to a list since that is how the :attr:`to` attribute tracks it.
       Similar logic is used for :attr:`cc` and :attr:`bcc`.

    All attributes shown below may also be specified via constructor.

    .. attribute:: key

       Unique key indicating the "type" of message.  An "ad-hoc"
       message created arbitrarily may not have/need a key; however
       one created via
       :meth:`~wuttjamaican.email.handler.EmailHandler.make_auto_message()`
       will always have a key.

       This key is not used for anything within the ``Message`` class
       logic.  It is used by
       :meth:`~wuttjamaican.email.handler.EmailHandler.make_auto_message()`
       when constructing the message, and the key is set on the final
       message only as a reference.

    .. attribute:: sender

       Sender (``From:``) address for the message.

    .. attribute:: subject

       Subject text for the message.

    .. attribute:: to

       List of ``To:`` recipients for the message.

    .. attribute:: cc

       List of ``Cc:`` recipients for the message.

    .. attribute:: bcc

       List of ``Bcc:`` recipients for the message.

    .. attribute:: replyto

       Optional reply-to (``Reply-To:``) address for the message.

    .. attribute:: txt_body

       String with the ``text/plain`` body content.

    .. attribute:: html_body

       String with the ``text/html`` body content.
    """

    def __init__(
            self,
            key=None,
            sender=None,
            subject=None,
            to=None,
            cc=None,
            bcc=None,
            replyto=None,
            txt_body=None,
            html_body=None,
    ):
        self.key = key
        self.sender = sender
        self.subject = subject
        self.set_recips('to', to)
        self.set_recips('cc', cc)
        self.set_recips('bcc', bcc)
        self.replyto = replyto
        self.txt_body = txt_body
        self.html_body = html_body

    def set_recips(self, name, value):
        """ """
        if value:
            if isinstance(value, str):
                value = [value]
            if not isinstance(value, (list, tuple)):
                raise ValueError("must specify a string, tuple or list value")
        else:
            value = []
        setattr(self, name, list(value))

    def as_string(self):
        """
        Returns the complete message as string.  This is called from
        within
        :meth:`~wuttjamaican.email.handler.EmailHandler.deliver_message()`
        to obtain the SMTP payload.
        """
        msg = None

        if self.txt_body and self.html_body:
            txt = MIMEText(self.txt_body, _charset='utf_8')
            html = MIMEText(self.html_body, _subtype='html', _charset='utf_8')
            msg = MIMEMultipart(_subtype='alternative', _subparts=[txt, html])

        elif self.txt_body:
            msg = MIMEText(self.txt_body, _charset='utf_8')

        elif self.html_body:
            msg = MIMEText(self.html_body, 'html', _charset='utf_8')

        if not msg:
            raise ValueError("message has no body parts")

        msg['Subject'] = self.subject
        msg['From'] = self.sender

        for addr in self.to:
            msg['To'] = addr
        for addr in self.cc:
            msg['Cc'] = addr
        for addr in self.bcc:
            msg['Bcc'] = addr

        if self.replyto:
            msg.add_header('Reply-To', self.replyto)

        return msg.as_string()
