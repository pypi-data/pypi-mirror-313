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
WuttJamaican - command line interface

See also :doc:`/narr/cli/index`.

This (``wuttjamaican.cli``) namespace exposes the following:

* :func:`~wuttjamaican.cli.base.make_typer`
* :data:`~wuttjamaican.cli.base.wutta_typer` (top-level command)
"""

from .base import wutta_typer, make_typer

# TODO: is this the best we can do, to register available commands?
from . import make_uuid
