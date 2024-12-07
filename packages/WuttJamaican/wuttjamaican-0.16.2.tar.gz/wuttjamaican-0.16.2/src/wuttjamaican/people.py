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
People Handler

This is a :term:`handler` to manage "people" in the DB.
"""

from wuttjamaican.app import GenericHandler


class PeopleHandler(GenericHandler):
    """
    Base class and default implementation for the "people"
    :term:`handler`.

    This is responsible for managing
    :class:`~wuttjamaican.db.model.base.Person` records, and related
    things.
    """

    def get_person(self, obj, **kwargs):
        """
        Return the :class:`~wuttjamaican.db.model.base.Person`
        associated with the given object, if one can be found.

        This method should accept "any" type of ``obj`` and inspect it
        to determine if/how a person can be found.  It should return
        the "first, most obvious" person in the event that the object
        is associated with multiple people.

        This is a rather fundamental method, in that it is called by
        several other methods, both within this handler as well as
        others.  There is also a shortcut to it, accessible via
        :meth:`wuttjamaican.app.AppHandler.get_person()`.
        """
        model = self.app.model

        if isinstance(obj, model.Person):
            person = obj
            return person

        elif isinstance(obj, model.User):
            user = obj
            if user.person:
                return user.person
