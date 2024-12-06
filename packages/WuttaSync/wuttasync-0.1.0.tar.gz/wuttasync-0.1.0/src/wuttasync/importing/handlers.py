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
Data Import / Export Handlers
"""

import logging
from collections import OrderedDict
from enum import Enum

from wuttjamaican.app import GenericHandler


log = logging.getLogger(__name__)


class Orientation(Enum):
    """
    Enum values for :attr:`ImportHandler.orientation`.
    """
    IMPORT = 'import'
    EXPORT = 'export'


class ImportHandler(GenericHandler):
    """
    Base class for all import/export handlers.

    Despite the name ``ImportHandler`` this can be used for export as
    well.  The logic is no different on a technical level and the
    "export" concept is mostly only helpful to the user.  The latter
    is important of course and to help with that we track the
    :attr:`orientation` to distinguish.

    The role of the "import/export handler" (instance of this class)
    is to orchestrate the overall DB connections, transactions and
    then invoke the importer/exporter instance(s) to do the actual
    data assessment/transfer.  Each of the latter will be an instance
    of (a subclass of) :class:`~wuttasync.importing.base.Importer`.
    """

    source_key = None
    """
    Key identifier for the data source.

    This should "uniquely" identify the data source, within the
    context of the data target.  For instance in the case of CSV →
    Wutta, ``csv`` is the source key.

    Among other things, this value is used in :meth:`get_key()`.
    """

    target_key = None
    """
    Key identifier for the data target.

    This should "uniquely" identify the data target.  For instance in
    the case of CSV → Wutta, ``wutta`` is the target key.

    Among other things, this value is used in :meth:`get_key()`.
    """

    orientation = Orientation.IMPORT
    """
    Orientation for the data flow.  Must be a value from
    :enum:`Orientation`:

    * ``Orientation.IMPORT`` (aka. ``'import'``)
    * ``Orientation.EXPORT`` (aka. ``'export'``)

    Note that the value may be displayed to the user where helpful::

       print(handler.orientation.value)

    See also :attr:`actioning`.

    It's important to understand the difference between import/export
    and source/target; they are independent concepts.  Source and
    target indicate where data comes from and where it's going,
    whereas import vs. export is mostly cosmetic.

    How a given data flow's orientation is determined, is basically up
    to the developer.  Most of the time it is straightforward,
    e.g. CSV → Wutta would be import, and Wutta → CSV would be
    export.  But confusing edge cases certainly exist, you'll know
    them when you see them.  In those cases the developer should try
    to choose whichever the end user is likely to find less confusing.
    """

    dry_run = False
    """
    Flag indicating whether data import/export should truly happen vs.
    dry-run only.

    If true, the data transaction will be rolled back at the end; if
    false then it will be committed.

    See also :meth:`rollback_transaction()` and
    :meth:`commit_transaction()`.
    """

    importers = None
    """
    This should be a dict of all importer/exporter classes available
    to the handler.  Keys are "model names" and each value is an
    importer/exporter class.  For instance::

       {
           'Widget': WidgetImporter,
       }

    This dict is defined during the handler constructor; see also
    :meth:`define_importers()`.

    Note that in practice, this is usually an ``OrderedDict`` so that
    the "sorting" of importer/exporters can be curated.

    If you want an importer/exporter instance you should not use this
    directly but instead call :meth:`get_importer()`.
    """

    def __init__(self, config, **kwargs):
        """ """
        super().__init__(config, **kwargs)
        self.importers = self.define_importers()

    def __str__(self):
        """ """
        return self.get_title()

    @property
    def actioning(self):
        """
        Convenience property which effectively returns the
        :attr:`orientation` in progressive verb tense - i.e. one of:

        * ``'importing'``
        * ``'exporting'``
        """
        return f'{self.orientation.value}ing'

    @classmethod
    def get_key(cls):
        """
        Returns the "full key" for the handler.  This is a combination
        of :attr:`source_key` and :attr:`target_key` and
        :attr:`orientation`.

        For instance in the case of CSV → Wutta, the full handler key
        is ``to_wutta.from_csv.import``.

        Note that more than one handler may return the same full key
        here; but only one will be configured as the "default" handler
        for that key.  See also :meth:`get_spec()`.
        """
        return f'to_{cls.target_key}.from_{cls.source_key}.{cls.orientation.value}'

    @classmethod
    def get_spec(cls):
        """
        Returns the "class spec" for the handler.  This value is the
        same as what might be used to configure the default handler
        for a given key.

        For instance in the case of CSV → Wutta, the default handler
        spec is ``wuttasync.importing.csv:FromCsvToWutta``.

        See also :meth:`get_key()`.
        """
        return f'{cls.__module__}:{cls.__name__}'

    def get_title(self):
        """
        Returns the full display title for the handler, e.g. ``"CSV →
        Wutta"``.

        Note that the :attr:`orientation` is not included in this title.

        It calls :meth:`get_source_title()` and
        :meth:`get_target_title()` to construct the full title.
        """
        source = self.get_source_title()
        target = self.get_target_title()
        return f"{source} → {target}"

    def get_source_title(self):
        """
        Returns the display title for the data source.

        See also :meth:`get_title()` and :meth:`get_target_title()`.
        """
        if hasattr(self, 'source_title'):
            return self.source_title
        if hasattr(self, 'generic_source_title'):
            return self.generic_source_title
        return self.source_key

    def get_target_title(self):
        """
        Returns the display title for the data target.

        See also :meth:`get_title()` and :meth:`get_source_title()`.
        """
        if hasattr(self, 'target_title'):
            return self.target_title
        if hasattr(self, 'generic_target_title'):
            return self.generic_target_title
        return self.target_key

    def process_data(self, *keys, **kwargs):
        """
        Run import/export operations for the specified models.

        :param \*keys: One or more importer/exporter (model) keys, as
           defined by the handler.

        Each key specified must be present in :attr:`importers` and
        thus will correspond to an importer/exporter class.

        A transaction is begun on the source and/or target side as
        needed, then for each model key requested, the corresponding
        importer/exporter is created and invoked.  And finally the
        transaction is committed (assuming normal operation).

        See also these methods which may be called from this one:

        * :meth:`consume_kwargs()`
        * :meth:`begin_transaction()`
        * :meth:`get_importer()`
        * :meth:`~wuttasync.importing.base.Importer.process_data()` (on the importer/exporter)
        * :meth:`rollback_transaction()`
        * :meth:`commit_transaction()`
        """
        kwargs = self.consume_kwargs(kwargs)
        self.begin_transaction()

        success = False
        try:

            # loop thru specified importer keys
            for key in keys:

                # invoke importer
                importer = self.get_importer(key, **kwargs)
                created, updated, deleted = importer.process_data()

                # log what happened
                msg = "%s: added %d; updated %d; deleted %d %s records"
                if self.dry_run:
                    msg += " (dry run)"
                log.info(msg, self.get_title(), len(created), len(updated), len(deleted), key)

        except:
            # TODO: what should happen here?
            raise

        else:
            success = True

        finally:
            if not success:
                log.warning("something failed, so transaction was rolled back")
                self.rollback_transaction()
            elif self.dry_run:
                log.info("dry run, so transaction was rolled back")
                self.rollback_transaction()
            else:
                log.info("transaction was committed")
                self.commit_transaction()

    def consume_kwargs(self, kwargs):
        """
        This method is called by :meth:`process_data()`.

        Its purpose is to give handlers a hook by which they can
        update internal handler state from the given kwargs, prior to
        running the import/export task(s).

        Any kwargs which pertain only to the handler, should be
        removed before they are returned.  But any kwargs which (also)
        may pertain to the importer/exporter instance, should *not* be
        removed, so they are passed along via :meth:`get_importer()`.

        :param kwargs: Dict of kwargs, "pre-consumption."  This is the
           same kwargs dict originally received by
           :meth:`process_data()`.

        :returns: Dict of kwargs, "post-consumption."
        """
        if 'dry_run' in kwargs:
            self.dry_run = kwargs['dry_run']

        return kwargs

    def begin_transaction(self):
        """
        Begin an import/export transaction, on source and/or target
        side as needed.

        This is normally called from :meth:`process_data()`.

        Default logic will call both:

        * :meth:`begin_source_transaction()`
        * :meth:`begin_target_transaction()`
        """
        self.begin_source_transaction()
        self.begin_target_transaction()

    def begin_source_transaction(self):
        """
        Begin a transaction on the source side, if applicable.

        This is normally called from :meth:`begin_transaction()`.
        """

    def begin_target_transaction(self):
        """
        Begin a transaction on the target side, if applicable.

        This is normally called from :meth:`begin_transaction()`.
        """

    def commit_transaction(self):
        """
        Commit the current import/export transaction, on source and/or
        target side as needed.

        This is normally called from :meth:`process_data()`.

        Default logic will call both:

        * :meth:`commit_target_transaction()`
        * :meth:`commit_source_transaction()`

        .. note::

           By default the target transaction is committed first; this
           is to avoid edge case errors when the source connection
           times out.  In such cases we want to properly cleanup the
           target and then if an error happens when trying to cleanup
           the source, it is less disruptive.
        """
        # nb. it can sometimes be important to commit the target
        # transaction first.  in particular when the import takes a
        # long time, it may be that no activity occurs on the source
        # DB session after the initial data read.  then at the end
        # committing the source transaction may trigger a connection
        # timeout error, which then prevents target transaction from
        # committing.  so now we just commit target first instead.
        # TODO: maybe sequence should be configurable?
        self.commit_target_transaction()
        self.commit_source_transaction()

    def commit_source_transaction(self):
        """
        Commit the transaction on the source side, if applicable.

        This is normally called from :meth:`commit_transaction()`.
        """

    def commit_target_transaction(self):
        """
        Commit the transaction on the target side, if applicable.

        This is normally called from :meth:`commit_transaction()`.
        """

    def rollback_transaction(self):
        """
        Rollback the current import/export transaction, on source
        and/or target side as needed.

        This is normally called from :meth:`process_data()`.  It is
        "always" called when :attr:`dry_run` is true, but also may be
        called if errors are encountered.

        Default logic will call both:

        * :meth:`rollback_target_transaction()`
        * :meth:`rollback_source_transaction()`

        .. note::

           By default the target transaction is rolled back first;
           this is to avoid edge case errors when the source
           connection times out.  In such cases we want to properly
           cleanup the target and then if an error happens when trying
           to cleanup the source, it is less disruptive.
        """
        # nb. it can sometimes be important to rollback the target
        # transaction first.  in particular when the import takes a
        # long time, it may be that no activity occurs on the source
        # DB session after the initial data read.  then at the end
        # rolling back the source transaction may trigger a connection
        # timeout error, which then prevents target transaction from
        # being rolled back.  so now we always rollback target first.
        # TODO: maybe sequence should be configurable?
        self.rollback_target_transaction()
        self.rollback_source_transaction()

    def rollback_source_transaction(self):
        """
        Rollback the transaction on the source side, if applicable.

        This is normally called from :meth:`rollback_transaction()`.
        """

    def rollback_target_transaction(self):
        """
        Rollback the transaction on the target side, if applicable.

        This is normally called from :meth:`rollback_transaction()`.
        """

    def define_importers(self):
        """
        This method must "define" all importer/exporter classes
        available to the handler.  It is called from the constructor.

        This should return a dict keyed by "model name" and each value
        is an importer/exporter class.  The end result is then
        assigned as :attr:`importers` (in the constoructor).

        For instance::

           return {
               'Widget': WidgetImporter,
           }

        Note that the model name will be displayed in various places
        and the caller may invoke a specific importer/exporter by this
        name etc.  See also :meth:`get_importer()`.
        """
        return OrderedDict()

    def get_importer(self, key, **kwargs):
        """
        Returns an importer/exporter instance corresponding to the
        given key.

        The key will be the "model name" mapped to a particular
        importer/exporter class and thus must be present in
        :attr:`importers`.

        This method is called from :meth:`process_data()` but may also
        be used by ad-hoc callers elsewhere.

        It will call :meth:`get_importer_kwargs()` and then construct
        the importer/exporter instance using those kwargs.

        :param key: Model key for desired importer/exporter.

        :returns: Instance of (subclass of)
           :class:`~wuttasync.importing.base.Importer`.
        """
        if key not in self.importers:
            orientation = self.orientation.value
            raise KeyError(f"unknown {orientation} key: {key}")

        kwargs = self.get_importer_kwargs(key, **kwargs)
        kwargs['handler'] = self
        factory = self.importers[key]
        return factory(self.config, **kwargs)

    def get_importer_kwargs(self, key, **kwargs):
        """
        Returns a dict of kwargs to be used when construcing an
        importer/exporter with the given key.  This is normally called
        from :meth:`get_importer()`.

        :param key: Model key for the desired importer/exporter,
           e.g. ``'Widget'``

        :param \**kwargs: Any kwargs we have so collected far.

        :returns: Final kwargs dict for new importer/exporter.
        """
        return kwargs


class FromFileHandler(ImportHandler):
    """
    Handler for import/export which uses an input file as data source.
    """


class ToSqlalchemyHandler(ImportHandler):
    """
    Handler for import/export which targets a SQLAlchemy ORM (DB).
    """

    target_session = None
    """
    Reference to the SQLAlchemy :term:`db session` for the target side.

    This may often be a session for the :term:`app database` (i.e. for
    importing to Wutta DB) but it could also be any other.

    This will be ``None`` unless an import/export transaction is
    underway.  See also :meth:`begin_target_transaction()`.
    """

    def begin_target_transaction(self):
        """
        Establish a new :term:`db session` via
        :meth:`make_target_session()` and assign the result to
        :attr:`target_session`.
        """
        self.target_session = self.make_target_session()

    def rollback_target_transaction(self):
        """
        Rollback the :attr:`target_session`.
        """
        self.target_session.rollback()
        self.target_session.close()
        self.target_session = None

    def commit_target_transaction(self):
        """
        Commit the :attr:`target_session`.
        """
        self.target_session.commit()
        self.target_session.close()
        self.target_session = None

    def make_target_session(self):
        """
        Make and return a new :term:`db session` for the import/export.

        Subclass must override this; default logic is not implemented.
        """
        raise NotImplementedError

    def get_importer_kwargs(self, key, **kwargs):
        """ """
        kwargs = super().get_importer_kwargs(key, **kwargs)
        kwargs.setdefault('target_session', self.target_session)
        return kwargs
