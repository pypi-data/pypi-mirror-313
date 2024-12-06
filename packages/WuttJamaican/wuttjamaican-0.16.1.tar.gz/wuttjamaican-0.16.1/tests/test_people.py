# -*- coding: utf-8; -*-

from wuttjamaican import people as mod
from wuttjamaican.testing import DataTestCase

try:
    import sqlalchemy as sa
except ImportError:
    pass
else:


    class TestPeopleHandler(DataTestCase):

        def make_handler(self):
            return mod.PeopleHandler(self.config)

        def test_get_person(self):
            model = self.app.model
            myperson = model.Person(full_name='Barny Rubble')
            self.session.add(myperson)
            self.session.commit()
            handler = self.make_handler()

            # empty obj is ignored
            person = handler.get_person(None)
            self.assertIsNone(person)

            # person is returned as-is
            person = handler.get_person(myperson)
            self.assertIs(person, myperson)

            # find person from user
            myuser = model.User(username='barney', person=myperson)
            self.session.add(myuser)
            self.session.commit()
            person = handler.get_person(myuser)
            self.assertIs(person, myperson)
