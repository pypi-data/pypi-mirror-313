# -*- coding: utf-8; -*-

from unittest import TestCase

try:
    from wuttjamaican.db.model import base as mod
    from wuttjamaican.db.model.auth import User
except ImportError:
    pass
else:

    class TestSetting(TestCase):

        def test_basic(self):
            setting = mod.Setting()
            self.assertEqual(str(setting), "")
            setting.name = 'foo'
            self.assertEqual(str(setting), "foo")

    class TestPerson(TestCase):

        def test_basic(self):
            person = mod.Person()
            self.assertEqual(str(person), "")
            person.full_name = "Barney Rubble"
            self.assertEqual(str(person), "Barney Rubble")

        def test_users(self):
            person = mod.Person()
            self.assertIsNone(person.user)

            user = User()
            person.users.append(user)
            self.assertIs(person.user, user)
