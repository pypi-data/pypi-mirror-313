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
Importing from CSV
"""

import csv
from collections import OrderedDict

from sqlalchemy_utils.functions import get_primary_keys

from wuttjamaican.db.util import make_topo_sortkey

from .base import FromFile
from .handlers import FromFileHandler
from .wutta import ToWuttaHandler
from .model import ToWutta


class FromCsv(FromFile):
    """
    Base class for importer/exporter using CSV file as data source.

    Note that this assumes a particular "format" for the CSV files.
    If your needs deviate you should override more methods, e.g.
    :meth:`open_input_file()`.

    The default logic assumes CSV file is mostly "standard" - e.g.
    comma-delimited, UTF-8-encoded etc.  But it also assumes the first
    line/row in the file contains column headers, and all subsequent
    lines are data rows.

    .. attribute:: input_reader

       While the input file is open, this will reference a
       :class:`python:csv.DictReader` instance.
    """

    csv_encoding = 'utf_8'
    """
    Encoding used by the CSV input file.

    You can specify an override if needed when calling
    :meth:`~wuttasync.importing.handlers.ImportHandler.process_data()`.
    """

    def get_input_file_name(self):
        """
        By default this returns the importer/exporter model name plus
        CSV file extension, e.g. ``Widget.csv``

        It calls
        :meth:`~wuttasync.importing.base.Importer.get_model_title()`
        to obtain the model name.
        """
        if hasattr(self, 'input_file_name'):
            return self.input_file_name

        model_title = self.get_model_title()
        return f'{model_title}.csv'

    def open_input_file(self):
        """
        Open the input file for reading, using a CSV parser.

        This tracks the file handle via
        :attr:`~wuttasync.importing.base.FromFile.input_file` and the
        CSV reader via :attr:`input_reader`.
        """
        path = self.get_input_file_path()
        self.input_file = open(path, 'rt', encoding=self.csv_encoding)
        self.input_reader = csv.DictReader(self.input_file)

    def close_input_file(self):
        """ """
        self.input_file.close()
        del self.input_reader
        del self.input_file

    def get_source_objects(self):
        """
        This returns a list of data records "as-is" from the CSV
        source file (via :attr:`input_reader`).

        Since this uses :class:`python:csv.DictReader` by default,
        each record will be a dict with key/value for each column in
        the file.
        """
        return list(self.input_reader)


class FromCsvToSqlalchemyMixin:
    """
    Mixin handler class for CSV → SQLAlchemy ORM import/export.
    """
    source_key = 'csv'
    generic_source_title = "CSV"

    FromImporterBase = FromCsv
    """
    This must be set to a valid base class for the CSV source side.
    Default is :class:`FromCsv` which should typically be fine; you
    can change if needed.
    """

    # nb. subclass must define this
    ToImporterBase = None
    """
    For a handler to use this mixin, this must be set to a valid base
    class for the ORM target side.  The :meth:`define_importers()`
    logic will use this as base class when dynamically generating new
    importer/exporter classes.
    """

    def get_target_model(self):
        """
        This should return the :term:`app model` or a similar module
        containing data model classes for the target side.

        The target model is used to dynamically generate a set of
        importers (e.g. one per table in the target DB) which can use
        CSV file as data source.  See also :meth:`define_importers()`.

        Subclass must override this if needed; default behavior is not
        implemented.
        """
        raise NotImplementedError

    def define_importers(self):
        """
        This mixin overrides typical (manual) importer definition, and
        instead dynamically generates a set of importers, e.g. one per
        table in the target DB.

        It does this based on the target model, as returned by
        :meth:`get_target_model()`.  It calls
        :meth:`make_importer_factory()` for each model class found.
        """
        importers = {}
        model = self.get_target_model()

        # mostly try to make an importer for every data model
        for name in dir(model):
            cls = getattr(model, name)
            if isinstance(cls, type) and issubclass(cls, model.Base) and cls is not model.Base:
                importers[name] = self.make_importer_factory(cls, name)

        # sort importers according to schema topography
        topo_sortkey = make_topo_sortkey(model)
        importers = OrderedDict([
            (name, importers[name])
            for name in sorted(importers, key=topo_sortkey)
        ])

        return importers

    def make_importer_factory(self, cls, name):
        """
        Generate and return a new importer/exporter class, targeting
        the given data model class.

        :param cls: A data model class.

        :param name: Optional "model name" override for the
           importer/exporter.

        :returns: A new class, meant to process import/export
           operations which target the given data model.  The new
           class will inherit from both :attr:`FromImporterBase` and
           :attr:`ToImporterBase`.
        """
        return type(f'{name}Importer', (FromCsv, self.ToImporterBase), {
            'model_class': cls,
            'key': list(get_primary_keys(cls)),
        })


class FromCsvToWutta(FromCsvToSqlalchemyMixin, ToWuttaHandler):
    """
    Handler for CSV → Wutta :term:`app database` import.
    """
    ToImporterBase = ToWutta

    def get_target_model(self):
        """ """
        return self.app.model
