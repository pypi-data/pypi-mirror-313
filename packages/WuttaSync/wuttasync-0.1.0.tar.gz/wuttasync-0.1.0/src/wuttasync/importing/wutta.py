# -*- coding: utf-8; -*-
################################################################################
#
#  WuttaSync -- Wutta framework for data import/export and real-time sync
#  Copyright © 2024 Lance Edgar
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
Wutta ⇄ Wutta import/export
"""

from .handlers import ToSqlalchemyHandler


class ToWuttaHandler(ToSqlalchemyHandler):
    """
    Handler for import/export which targets Wutta ORM (:term:`app
    database`).
    """

    target_key = 'wutta'
    "" # nb. suppress docs

    def get_target_title(self):
        """ """
        # nb. we override parent to use app title as default
        if hasattr(self, 'target_title'):
            return self.target_title
        if hasattr(self, 'generic_target_title'):
            return self.generic_target_title
        return self.app.get_title()

    def make_target_session(self):
        """
        Call
        :meth:`~wuttjamaican:wuttjamaican.app.AppHandler.make_session()`
        and return the result.

        :returns: :class:`~wuttjamaican:wuttjamaican.db.sess.Session`
           instance.
        """
        return self.app.make_session()
