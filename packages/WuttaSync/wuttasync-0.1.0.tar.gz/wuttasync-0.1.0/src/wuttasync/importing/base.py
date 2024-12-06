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
Data Importer base class
"""

import os
import logging

from sqlalchemy import orm
from sqlalchemy_utils.functions import get_primary_keys, get_columns

from wuttasync.util import data_diffs


log = logging.getLogger(__name__)


class Importer:
    """
    Base class for all data importers / exporters.

    So as with :class:`~wuttasync.importing.handlers.ImportHandler`,
    despite the name ``Importer`` this class can be used for export as
    well.  Occasionally it's helpful to know "which mode" is in
    effect, mostly for display to the user.  See also
    :attr:`orientation` and :attr:`actioning`.

    The role of the "importer/exporter" (instance of this class) is to
    process the import/export of data for **one "model"** - which
    generally speaking, means one table.  Whereas the "import/export
    handler" (:class:`~wuttasync.importing.handlers.ImportHandler`
    instance) orchestrates the overall DB connections, transactions
    and invokes the importer(s)/exporter(s).  So multiple
    importers/exporters may run in the context of a single handler
    job.

    .. attribute:: handler

       Reference to the parent
       :class:`~wuttasync.importing.handlers.ImportHandler` instance.

    .. attribute:: model_class

       Reference to the :term:`data model` class representing the
       target side, if applicable.

       This normally would be a SQLAlchemy mapped class, e.g.
       :class:`~wuttjamaican:wuttjamaican.db.model.base.Person` for
       importing to the Wutta People table.

       It is primarily (only?) used when the target side of the
       import/export uses SQLAlchemy ORM.
    """

    allow_create = True
    """
    Flag indicating whether this importer/exporter should *ever* allow
    records to be created on the target side.

    This flag is typically defined in code for each handler.

    See also :attr:`create`.
    """

    allow_update = True
    """
    Flag indicating whether this importer/exporter should *ever* allow
    records to be updated on the target side.

    This flag is typically defined in code for each handler.

    See also :attr:`update`.
    """

    allow_delete = True
    """
    Flag indicating whether this importer/exporter should *ever* allow
    records to be deleted on the target side.

    This flag is typically defined in code for each handler.

    See also :attr:`delete`.
    """

    create = None
    """
    Flag indicating the current import/export job should create
    records on the target side, when applicable.

    This flag is typically set by the caller, e.g. via command line
    args.

    See also :attr:`allow_create`.
    """

    update = None
    """
    Flag indicating the current import/export job should update
    records on the target side, when applicable.

    This flag is typically set by the caller, e.g. via command line
    args.

    See also :attr:`allow_update`.
    """

    delete = None
    """
    Flag indicating the current import/export job should delete
    records on the target side, when applicable.

    This flag is typically set by the caller, e.g. via command line
    args.

    See also :attr:`allow_delete`.
    """

    caches_target = False
    """
    Flag indicating the importer/exporter should pre-fetch the
    existing target data.  This is usually what we want, so both
    source and target data sets are held in memory and lookups may be
    done between them without additional fetching.

    When this flag is false, the importer/exporter must query the
    target for every record it gets from the source data, when looking
    for a match.
    """

    cached_target = False
    """
    This is ``None`` unless :attr:`caches_target` is true, in which
    case it may (at times) hold the result from
    :meth:`get_target_cache()`.
    """

    def __init__(self, config, **kwargs):
        self.config = config
        self.app = self.config.get_app()

        self.create = kwargs.pop('create',
                                 kwargs.pop('allow_create', self.allow_create))
        self.update = kwargs.pop('update',
                                 kwargs.pop('allow_update', self.allow_update))
        self.delete = kwargs.pop('delete',
                                 kwargs.pop('allow_delete', self.allow_delete))

        self.__dict__.update(kwargs)

        self.simple_fields = self.get_simple_fields()
        self.supported_fields = self.get_supported_fields()
        self.fields = self.get_fields()

    @property
    def orientation(self):
        """
        Convenience property which returns the value of
        :attr:`wuttasync.importing.handlers.ImportHandler.orientation`
        from the parent import/export handler.
        """
        return self.handler.orientation

    @property
    def actioning(self):
        """
        Convenience property which returns the value of
        :attr:`wuttasync.importing.handlers.ImportHandler.actioning`
        from the parent import/export handler.
        """
        return self.handler.actioning

    @property
    def dry_run(self):
        """
        Convenience property which returns the value of
        :attr:`wuttasync.importing.handlers.ImportHandler.dry_run`
        from the parent import/export handler.
        """
        return self.handler.dry_run

    def get_model_title(self):
        """
        Returns the display title for the target data model.
        """
        if hasattr(self, 'model_title'):
            return self.model_title

        # TODO: this will fail if not using a model class, obviously..
        # should raise more helpful error msg?
        return self.model_class.__name__

    def get_simple_fields(self):
        """
        This should return a (possibly empty) list of "simple" fields
        for the import/export.  A "simple" field is one where the
        value is a simple scalar, so e.g. can use ``getattr(obj,
        field)`` to read and ``setattr(obj, field, value)`` to write.

        See also :meth:`get_supported_fields()` and
        :meth:`get_fields()`.

        :returns: Possibly empty list of "simple" field names.
        """
        if hasattr(self, 'simple_fields'):
            return self.simple_fields

        fields = get_columns(self.model_class)
        return list(fields.keys())

    def get_supported_fields(self):
        """
        This should return the full list of fields which are available
        for the import/export.

        Note that this field list applies first and foremost to the
        target side, i.e. if the target (table etc.) has no "foo"
        field defined then it should not be listed here.

        But it also applies to the source side, e.g. if target *does*
        define a "foo" field but source does not, then it again should
        not be listed here.

        See also :meth:`get_simple_fields()` and :meth:`get_fields()`.

        :returns: List of all "supported" field names.
        """
        if hasattr(self, 'supported_fields'):
            return self.supported_fields

        return self.get_simple_fields()

    def get_fields(self):
        """
        This should return the "effective" list of fields which are to
        be used for the import/export.

        All fields in this list should also be found in the output for
        :meth:`get_supported_fields()`.

        See also :meth:`get_keys()` and :meth:`get_simple_fields()`.

        :returns: List of "effective" field names.
        """
        if hasattr(self, 'fields'):
            return self.fields

        return self.get_supported_fields()

    def get_keys(self):
        """
        Must return the key field(s) for use with import/export.

        All fields in this list should also be found in the output for
        :meth:`get_fields()`.

        :returns: List of "key" field names.
        """
        if hasattr(self, 'key'):
            keys = self.key
            if isinstance(keys, str):
                keys = [keys]
            return keys

        return list(get_primary_keys(self.model_class))

    def setup(self):
        """
        Perform any setup needed before starting the import/export
        job.

        This is called from within :meth:`process_data()`.  Default
        logic does nothing.
        """

    def teardown(self):
        """
        Perform any teardown needed after ending the import/export
        job.

        This is called from within :meth:`process_data()`.  Default
        logic does nothing.
        """

    def process_data(self, source_data=None, progress=None):
        """
        Perform the data import/export operations on the target.

        This is the core feature logic and may create, update and/or
        delete records on the target side, depending on (subclass)
        implementation.  It is invoked directly by the parent
        :attr:`handler`.

        Note that subclass generally should not override this method,
        but instead some of the others.

        :param source_data: Optional sequence of normalized source
           data.  If not specified, it is obtained from
           :meth:`normalize_source_data()`.

        :param progress: Optional progress indicator factory.

        :returns: A 3-tuple of ``(created, updated, deleted)`` as
           follows:

           * ``created`` - list of records created on the target
           * ``updated`` - list of records updated on the target
           * ``deleted`` - list of records deleted on the target

        See also these methods which this one calls:

        * :meth:`setup()`
        * :meth:`do_create_update()`
        * :meth:`do_delete()`
        * :meth:`teardown()`
        """
        self.setup()
        created = []
        updated = []
        deleted = []

        # get complete set of normalized source data
        if source_data is None:
            source_data = self.normalize_source_data(progress=progress)

        # TODO: should exclude duplicate source records
        # source_data, unique = self.get_unique_data(source_data)

        # maybe cache existing target data
        if self.caches_target:
            self.cached_target = self.get_target_cache(source_data, progress=progress)

        # create and/or update target data
        if self.create or self.update:
            created, updated = self.do_create_update(source_data, progress=progress)

        # delete target data
        if self.delete:
            deleted = self.do_delete(source_data)

        self.teardown()
        return created, updated, deleted

    def do_create_update(self, all_source_data, progress=None):
        """
        Import/export the given normalized source data; create and/or
        update target records as needed.

        :param all_source_data: Sequence of all normalized source
           data, e.g. as obtained from
           :meth:`normalize_source_data()`.

        :param progress: Optional progress indicator factory.

        :returns: A 2-tuple of ``(created, updated)`` as follows:

           * ``created`` - list of records created on the target
           * ``updated`` - list of records updated on the target

        This loops through all source data records, and for each will
        try to find a matching target record.  If a match is found it
        also checks if any field values differ between them.  So,
        calls to these methods may also happen from here:

        * :meth:`get_record_key()`
        * :meth:`get_target_object()`
        * :meth:`create_target_object()`
        * :meth:`update_target_object()`
        """
        model_title = self.get_model_title()
        created = []
        updated = []

        # cache the set of fields to use for diff checks
        fields = set(self.get_fields()) - set(self.get_keys())

        def create_update(source_data, i):

            # try to fetch target object per source key
            key = self.get_record_key(source_data)
            target_object = self.get_target_object(key)
            if target_object and self.update:

                # target object exists, so compare data
                target_data = self.normalize_target_object(target_object)
                diffs = self.data_diffs(source_data, target_data, fields=fields)
                if diffs:

                    # data differs, so update target object
                    log.debug("fields (%s) differed for target data: %s and source data: %s",
                              ','.join(diffs), target_data, source_data)
                    target_object = self.update_target_object(target_object,
                                                              source_data,
                                                              target_data=target_data)
                    updated.append((target_object, target_data, source_data))

            elif not target_object and self.create:

                # target object not yet present, so create it
                target_object = self.create_target_object(key, source_data)
                if target_object:
                    log.debug("created new %s %s: %s", model_title, key, target_object)
                    created.append((target_object, source_data))
                    # TODO: update cache if applicable
                    # if self.caches_target and self.cached_target is not None:
                    #     self.cached_target[key] = {
                    #         'object': target_object,
                    #         'data': self.normalize_target_object(target_object),
                    #     }
                else:
                    log.debug("did NOT create new %s for key: %s", model_title, key)

        actioning = self.actioning.capitalize()
        target_title = self.handler.get_target_title()
        self.app.progress_loop(create_update, all_source_data, progress,
                               message=f"{actioning} {model_title} data to {target_title}")

        return created, updated

    def do_delete(self, source_data, progress=None):
        """
        TODO: not yet implemented

        :returns: List of records deleted on the target.
        """
        return []

    def get_record_key(self, data):
        """
        Returns the canonical key value for the given normalized data
        record.

        :param data: Normalized data record (dict).

        :returns: A tuple of field values, corresponding to the
           import/export key fields.

        Note that this calls :meth:`get_keys()` to determine the
        import/export key fields.

        So if an importer has ``key = 'id'`` then :meth:`get_keys()`
        would return ``('id',)`` and this method would return just the
        ``id`` value e.g. ``(42,)`` for the given data record.

        The return value is always a tuple for consistency and to
        allow for composite key fields.
        """
        return tuple(data[key] for key in self.get_keys())

    def data_diffs(self, source_data, target_data, fields=None):
        """
        Find all (relevant) fields with differing values between the
        two data records, source and target.

        This is a simple wrapper around
        :func:`wuttasync.util.data_diffs()` but unless caller
        specifies a ``fields`` list, this will use the following by
        default:

        It calls :meth:`get_fields()` to get the effective field list,
        and from that it *removes* the fields indicated by
        :meth:`get_keys()`.

        The thinking here, is that the goal of this function is to
        find true diffs, but any "key" fields will already match (or
        not) based on the overall processing logic and needn't be
        checked further.
        """

        if not fields:
            # nb. we do not check for diffs on the key fields, since
            # the source/target object matching already handles that
            # effectively.  also the uuid fields in particular can be
            # tricky, if target schema uses UUID proper but source
            # data represents them as string etc.
            fields = set(self.get_fields()) - set(self.get_keys())

        return data_diffs(source_data, target_data, fields=fields)

    ##############################
    # source methods
    ##############################

    def normalize_source_data(self, source_objects=None, progress=None):
        """
        This method must return the full list of normalized data
        records from the source.

        Default logic here will call :meth:`get_source_objects()` and
        then for each object :meth:`normalize_source_object_all()` is
        called.

        :param source_objects: Optional sequence of raw objects from
           the data source.  If not specified, it is obtained from
           :meth:`get_source_objects()`.

        :param progress: Optional progress indicator factory.

        :returns: List of normalized source data records.
        """
        if source_objects is None:
            source_objects = self.get_source_objects()
        normalized = []

        def normalize(obj, i):
            data = self.normalize_source_object_all(obj)
            if data:
                normalized.extend(data)

        model_title = self.get_model_title()
        source_title = self.handler.get_source_title()
        self.app.progress_loop(normalize, source_objects, progress,
                               message=f"Reading {model_title} data from {source_title}")
        return normalized

    def get_source_objects(self):
        """
        This method (if applicable) should return a sequence of "raw"
        data objects (i.e. non-normalized records) from the source.

        This method is typically called from
        :meth:`normalize_source_data()` which then also handles the
        normalization.
        """
        return []

    def normalize_source_object_all(self, obj):
        """
        This method should "iterate" over the given object and return
        a list of corresponding normalized data records.

        In most cases, the object is "singular" and it doesn't really
        make sense to return more than one data record for it.  But
        this method is here for subclass to override in those rare
        cases where you *do* need to "expand" the object into multiple
        source data records.

        Default logic for this method simply calls
        :meth:`normalize_source_object()` for the given object, and
        returns a list with just that one record.

        :param obj: Raw object from data source.

        :returns: List of normalized data records corresponding to the
           source object.
        """
        data = self.normalize_source_object(obj)
        if data:
            return [data]

    def normalize_source_object(self, obj):
        """
        This should return a single "normalized" data record for the
        given source object.

        Subclass will usually need to override this, to "convert"
        source data into the shared format required for import/export.
        The default logic merely returns the object as-is!

        Note that if this method returns ``None`` then the object is
        effectively skipped, treated like it does not exist on the
        source side.

        :param obj: Raw object from data source.

        :returns: Dict of normalized data fields, or ``None``.
        """
        return obj

    ##############################
    # target methods
    ##############################

    def get_target_cache(self, source_data=None, progress=None):
        """
        Fetch all (existing) raw objects and normalized data from the
        target side, and return a cache object with all of that.

        This method will call :meth:`get_target_objects()` first, and
        pass along the ``source_data`` param if specified.  From there
        it will call :meth:`normalize_target_object()` and
        :meth:`get_record_key()` for each.

        :param source_data: Sequence of normalized source data for the
           import/export job, if known.

        :param progress: Optional progress indicator factory.

        :returns: Dict whose keys are record keys (so one entry for
           every normalized target record) and the values are a nested
           dict with raw object and normalized record.

           A minimal but complete example of what this return value
           looks like::

              {
                  (1,): {
                      'object': <some_object_1>,
                      'data': {'id': 1, 'description': 'foo'},
                  }
                  (2,): {
                      'object': <some_object_2>,
                      'data': {'id': 2, 'description': 'bar'},
                  }
              }
        """
        objects = self.get_target_objects(source_data=source_data)
        cached = {}

        def cache(obj, i):
            data = self.normalize_target_object(obj)
            if data:
                key = self.get_record_key(data)
                cached[key] = {'object': obj, 'data': data}

        model_title = self.get_model_title()
        target_title = self.handler.get_target_title()
        self.app.progress_loop(cache, objects, progress,
                               message=f"Reading {model_title} data from {target_title}")
        return cached

    def get_target_objects(self, source_data=None, progress=None):
        """
        Fetch all existing raw objects from the data target.  Or at
        least, enough of them to satisfy matching on the given source
        data (if applicable).

        :param source_data: Sequence of normalized source data for the
           import/export job, if known.

        :param progress: Optional progress indicator factory.

        :returns: Corresponding sequence of raw objects from the
           target side.

        Note that the source data is provided only for cases where
        that might be useful; it often is not.

        But for instance if the source data contains say an ID field
        and the min/max values present in the data set are 1 thru 100,
        but the target side has millions of records, you might only
        fetch ID <= 100 from target side as an optimization.
        """
        raise NotImplementedError

    def get_target_object(self, key):
        """
        Should return the object from (existing) target data set which
        corresponds to the given record key, if found.

        Note that the default logic is able to find/return the object
        from :attr:`cached_target` if applicable.  But it is not able
        to do a one-off lookup e.g. in the target DB.  If you need the
        latter then you should override this method.

        :returns: Raw target data object, or ``None``.
        """
        if self.caches_target and self.cached_target is not None:
            cached = self.cached_target.get(key)
            return cached['object'] if cached else None

    def normalize_target_object(self, obj):
        """
        This should return a "normalized" data record for the given
        raw object from the target side.

        Subclass will often need to override this, to "convert" target
        object into the shared format required for import/export.  The
        default logic is only able to handle "simple" fields;
        cf. :meth:`get_simple_fields()`.

        It's possible to optimize this somewhat, by checking
        :meth:`get_fields()` and then normalization may be skipped for
        any fields which aren't "effective" for the current job.

        Note that if this method returns ``None`` then the object is
        ignored, treated like it does not exist on the target side.

        :param obj: Raw object from data target.

        :returns: Dict of normalized data fields, or ``None``.
        """
        fields = self.get_fields()
        fields = [f for f in self.get_simple_fields()
                  if f in fields]
        data = dict([(field, getattr(obj, field))
                     for field in fields])
        return data

    ##############################
    # CRUD methods
    ##############################

    def create_target_object(self, key, source_data):
        """
        Create and return a new target object for the given key, fully
        populated from the given source data.  This may return
        ``None`` if no object is created.

        This method will typically call :meth:`make_empty_object()`
        and then :meth:`update_target_object()`.

        :returns: New object for the target side, or ``None``.
        """
        if source_data.get('__ignoreme__'):
            return

        obj = self.make_empty_object(key)
        if obj:
            return self.update_target_object(obj, source_data)

    def make_empty_object(self, key):
        """
        Return a new empty target object for the given key.

        This method is called from :meth:`create_target_object()`.  It
        should only populate the object's key, and leave the rest of
        the fields to :meth:`update_target_object()`.

        Default logic will call :meth:`make_object()` to get the bare
        instance, then populate just the fields from
        :meth:`get_keys()`.
        """
        obj = self.make_object()
        for i, k in enumerate(self.get_keys()):
            if hasattr(obj, k):
                setattr(obj, k, key[i])
        return obj

    def make_object(self):
        """
        Make a bare target object instance.

        This method need not populate the object in any way.  See also
        :meth:`make_empty_object()`.

        Default logic will make a new instance of :attr:`model_class`.
        """
        return self.model_class()

    def update_target_object(self, obj, source_data, target_data=None):
        """
        Update the target object with the given source data, and
        return the updated object.

        This method may be called from :meth:`do_create_update()` for
        a normal update, or :meth:`create_target_object()` when
        creating a new record.

        It should update the object for any of :meth:`get_fields()`
        which appear to differ.  However it need not bother for the
        :meth:`get_keys()` fields, since those will already be
        accurate.

        :param obj: Raw target object.

        :param source_data: Dict of normalized data for source record.

        :param target_data: Dict of normalized data for existing
           target record, if a typical update.  Will be missing for a
           new object.

        :returns: The final updated object.  In most/all cases this
           will be the same instance as the original ``obj`` provided
           by the caller.
        """
        keys = self.get_keys()
        fields = self.get_fields()

        # we can automatically handle "simple" fields and update
        # target object where needed for those
        for field in self.get_simple_fields():

            if field in keys:
                # object key(s) should already be populated
                continue

            # elif field not in source_data:
            #     # no source data for field
            #     continue

            elif field in fields:

                # field is eligible for update generally, so compare
                # values between records
                if (not target_data
                    or field not in target_data
                    or target_data[field] != source_data[field]):

                    # data mismatch; update field for target object
                    setattr(obj, field, source_data[field])

        return obj


class FromFile(Importer):
    """
    Base class for importer/exporter using input file as data source.

    Depending on the subclass, it may be able to "guess" (at least
    partially) the path to the input file.  If not, and/or to avoid
    ambiguity, the caller must specify the file path.

    In most cases caller may specify any of these via kwarg to the
    class constructor, or e.g.
    :meth:`~wuttasync.importing.handlers.ImportHandler.process_data()`:

    * :attr:`input_file_path`
    * :attr:`input_file_dir`
    * :attr:`input_file_name`

    The subclass itself can also specify via override of these
    methods:

    * :meth:`get_input_file_path()`
    * :meth:`get_input_file_dir()`
    * :meth:`get_input_file_name()`

    And of course subclass must override these too:

    * :meth:`open_input_file()`
    * :meth:`close_input_file()`
    * (and see also :attr:`input_file`)

    .. attribute:: input_file_path

       Path to the input file.

    .. attribute:: input_file_dir

       Path to folder containing input file(s).

    .. attribute:: input_file_name

       Name of the input file, sans folder path.

    .. attribute:: input_file

       Handle to the open input file, if applicable.  May be set by
       :meth:`open_input_file()` for later reference within
       :meth:`close_input_file()`.
    """

    def setup(self):
        """
        Open the input file.  See also :meth:`open_input_file()`.
        """
        self.open_input_file()

    def teardown(self):
        """
        Close the input file.  See also :meth:`close_input_file()`.
        """
        self.close_input_file()

    def get_input_file_path(self):
        """
        This must return the full path to input file.  It tries to
        guess it based on various attributes, namely:

        * :attr:`input_file_path`
        * :attr:`input_file_dir`
        * :attr:`input_file_name`

        :returns: Path to input file.
        """
        if hasattr(self, 'input_file_path'):
            return self.input_file_path

        folder = self.get_input_file_dir()
        filename = self.get_input_file_name()
        return os.path.join(folder, filename)

    def get_input_file_dir(self):
        """
        This must return the folder with input file(s).  It tries to
        guess it based on various attributes, namely:

        * :attr:`input_file_dir`

        :returns: Path to folder with input file(s).
        """
        if hasattr(self, 'input_file_dir'):
            return self.input_file_dir

        raise NotImplementedError("can't guess path to input file(s) folder")

    def get_input_file_name(self):
        """
        This must return the input filename, sans folder path.  It
        tries to guess it based on various attributes, namely:

        * :attr:`input_file_name`

        :returns: Input filename, sans folder path.
        """
        if hasattr(self, 'input_file_name'):
            return self.input_file_name

        raise NotImplementedError("can't guess input filename")

    def open_input_file(self):
        """
        Open the input file for reading source data.

        Subclass must override to specify how this happens; default
        logic is not implemented.  Remember to set :attr:`input_file`
        if applicable for reference when closing.

        See also :attr:`get_input_file_path()` and
        :meth:`close_input_file()`.
        """
        raise NotImplementedError

    def close_input_file(self):
        """
        Close the input file for source data.

        Subclass must override to specify how this happens; default
        logic blindly calls the ``close()`` method on whatever
        :attr:`input_file` happens to point to.

        See also :attr:`open_input_file()`.
        """
        self.input_file.close()


class ToSqlalchemy(Importer):
    """
    Base class for importer/exporter which uses SQLAlchemy ORM on the
    target side.
    """

    caches_target = True
    "" # nb. suppress sphinx docs

    def get_target_object(self, key):
        """
        Tries to fetch the object from target DB using ORM query.
        """
        # first the default logic in case target object is cached
        obj = super().get_target_object(key)
        if obj:
            return obj

        # okay now we must fetch via query
        query = self.target_session.query(self.model_class)
        for i, k in enumerate(self.get_keys()):
            query = query.filter(getattr(self.model_class, k) == key[i])
        try:
            return query.one()
        except orm.exc.NoResultFound:
            pass

    def create_target_object(self, key, source_data):
        """ """
        with self.target_session.no_autoflush:
            obj = super().create_target_object(key, source_data)
        if obj:
            # nb. add new object to target db session
            self.target_session.add(obj)
            return obj

    def get_target_objects(self, source_data=None, progress=None):
        """
        Fetches target objects via the ORM query from
        :meth:`get_target_query()`.
        """
        query = self.get_target_query(source_data=source_data)
        return query.all()

    def get_target_query(self, source_data=None):
        """
        Returns an ORM query suitable to fetch existing objects from
        the target side.  This is called from
        :meth:`get_target_objects()`.
        """
        return self.target_session.query(self.model_class)
