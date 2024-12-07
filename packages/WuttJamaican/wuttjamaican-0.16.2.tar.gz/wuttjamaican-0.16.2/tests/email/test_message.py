# -*- coding: utf-8; -*-

from unittest import TestCase

from wuttjamaican.email import message as mod


class TestMessage(TestCase):

    def make_message(self, **kwargs):
        return mod.Message(**kwargs)

    def test_set_recips(self):
        msg = self.make_message()
        self.assertEqual(msg.to, [])

        # set as list
        msg.set_recips('to', ['sally@example.com'])
        self.assertEqual(msg.to, ['sally@example.com'])

        # set as tuple
        msg.set_recips('to', ('barney@example.com',))
        self.assertEqual(msg.to, ['barney@example.com'])

        # set as string
        msg.set_recips('to', 'wilma@example.com')
        self.assertEqual(msg.to, ['wilma@example.com'])

        # set as null
        msg.set_recips('to', None)
        self.assertEqual(msg.to, [])

        # otherwise error
        self.assertRaises(ValueError, msg.set_recips, 'to', {'foo': 'foo@example.com'})

    def test_as_string(self):

        # error if no body
        msg = self.make_message()
        self.assertRaises(ValueError, msg.as_string)

        # txt body
        msg = self.make_message(sender='bob@example.com',
                                txt_body="hello world")
        complete = msg.as_string()
        self.assertIn('From: bob@example.com', complete)

        # html body
        msg = self.make_message(sender='bob@example.com',
                                html_body="<p>hello world</p>")
        complete = msg.as_string()
        self.assertIn('From: bob@example.com', complete)

        # txt + html body
        msg = self.make_message(sender='bob@example.com',
                                txt_body="hello world",
                                html_body="<p>hello world</p>")
        complete = msg.as_string()
        self.assertIn('From: bob@example.com', complete)

        # everything
        msg = self.make_message(sender='bob@example.com',
                                subject='meeting follow-up',
                                to='sally@example.com',
                                cc='marketing@example.com',
                                bcc='bob@example.com',
                                replyto='sales@example.com',
                                txt_body="hello world",
                                html_body="<p>hello world</p>")
        complete = msg.as_string()
        self.assertIn('From: bob@example.com', complete)
        self.assertIn('Subject: meeting follow-up', complete)
        self.assertIn('To: sally@example.com', complete)
        self.assertIn('Cc: marketing@example.com', complete)
        self.assertIn('Bcc: bob@example.com', complete)
        self.assertIn('Reply-To: sales@example.com', complete)
