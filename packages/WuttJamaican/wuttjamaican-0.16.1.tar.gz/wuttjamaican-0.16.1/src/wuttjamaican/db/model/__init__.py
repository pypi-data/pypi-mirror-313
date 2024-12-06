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
Data Models

This is the default :term:`app model` module.

The ``wuttjamaican.db.model`` namespace contains the following:

* :class:`~wuttjamaican.db.model.base.Base`
* :class:`~wuttjamaican.db.model.base.Setting`
* :class:`~wuttjamaican.db.model.base.Person`
* :class:`~wuttjamaican.db.model.auth.Role`
* :class:`~wuttjamaican.db.model.auth.Permission`
* :class:`~wuttjamaican.db.model.auth.User`
* :class:`~wuttjamaican.db.model.auth.UserRole`
* :class:`~wuttjamaican.db.model.upgrades.Upgrade`
"""

# TODO: remove these
from wuttjamaican.db.util import uuid_column, uuid_fk_column

from .base import Base, Setting, Person
from .auth import Role, Permission, User, UserRole
from .upgrades import Upgrade
