#-*- coding: utf-8; -*-

from unittest.mock import patch

from wuttjamaican.testing import DataTestCase

from wuttasync.importing import base as mod, ImportHandler, Orientation


class TestImporter(DataTestCase):

    def setUp(self):
        self.setup_db()
        self.handler = ImportHandler(self.config)

    def make_importer(self, **kwargs):
        kwargs.setdefault('handler', self.handler)
        return mod.Importer(self.config, **kwargs)

    def test_constructor(self):
        model = self.app.model

        # basic importer
        imp = self.make_importer(model_class=model.Setting)

        # fields
        self.assertEqual(imp.supported_fields, ['name', 'value'])
        self.assertEqual(imp.simple_fields, ['name', 'value'])
        self.assertEqual(imp.fields, ['name', 'value'])

        # orientation etc.
        self.assertEqual(imp.orientation, Orientation.IMPORT)
        self.assertEqual(imp.actioning, 'importing')
        self.assertTrue(imp.create)
        self.assertTrue(imp.update)
        self.assertTrue(imp.delete)
        self.assertFalse(imp.dry_run)

    def test_get_model_title(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)
        self.assertEqual(imp.get_model_title(), 'Setting')
        imp.model_title = "SeTtInG"
        self.assertEqual(imp.get_model_title(), 'SeTtInG')

    def test_get_simple_fields(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)
        self.assertEqual(imp.get_simple_fields(), ['name', 'value'])
        imp.simple_fields = ['name']
        self.assertEqual(imp.get_simple_fields(), ['name'])

    def test_get_supported_fields(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)
        self.assertEqual(imp.get_supported_fields(), ['name', 'value'])
        imp.supported_fields = ['name']
        self.assertEqual(imp.get_supported_fields(), ['name'])

    def test_get_fields(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)
        self.assertEqual(imp.get_fields(), ['name', 'value'])
        imp.fields = ['name']
        self.assertEqual(imp.get_fields(), ['name'])

    def test_get_keys(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)
        self.assertEqual(imp.get_keys(), ['name'])
        imp.key = 'value'
        self.assertEqual(imp.get_keys(), ['value'])

    def test_process_data(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting, caches_target=True)

        # empty data set / just for coverage
        with patch.object(imp, 'normalize_source_data') as normalize_source_data:
            normalize_source_data.return_value = []

            with patch.object(imp, 'get_target_cache') as get_target_cache:
                get_target_cache.return_value = {}

                result = imp.process_data()
                self.assertEqual(result, ([], [], []))

    def test_do_create_update(self):
        model = self.app.model

        # this requires a mock target cache
        imp = self.make_importer(model_class=model.Setting, caches_target=True)
        setting = model.Setting(name='foo', value='bar')
        imp.cached_target = {
            ('foo',): {
                'object': setting,
                'data': {'name': 'foo', 'value': 'bar'},
            },
        }

        # will update the one record
        result = imp.do_create_update([{'name': 'foo', 'value': 'baz'}])
        self.assertIs(result[1][0][0], setting)
        self.assertEqual(result, ([], [(setting,
                                        # nb. target
                                        {'name': 'foo', 'value': 'bar'},
                                        # nb. source
                                        {'name': 'foo', 'value': 'baz'})]))
        self.assertEqual(setting.value, 'baz')

        # will create a new record
        result = imp.do_create_update([{'name': 'blah', 'value': 'zay'}])
        self.assertIsNot(result[0][0][0], setting)
        setting_new = result[0][0][0]
        self.assertEqual(result, ([(setting_new,
                                        # nb. source
                                        {'name': 'blah', 'value': 'zay'})],
                                  []))
        self.assertEqual(setting_new.name, 'blah')
        self.assertEqual(setting_new.value, 'zay')

        # but what if new record is *not* created
        with patch.object(imp, 'create_target_object', return_value=None):
            result = imp.do_create_update([{'name': 'another', 'value': 'one'}])
            self.assertEqual(result, ([], []))

    # def test_do_delete(self):
    #     model = self.app.model
    #     imp = self.make_importer(model_class=model.Setting)

    def test_get_record_key(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)
        record = {'name': 'foo', 'value': 'bar'}
        self.assertEqual(imp.get_record_key(record), ('foo',))
        imp.key = ('name', 'value')
        self.assertEqual(imp.get_record_key(record), ('foo', 'bar'))

    def test_data_diffs(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)

        # 2 identical records
        rec1 = {'name': 'foo', 'value': 'bar'}
        rec2 = {'name': 'foo', 'value': 'bar'}
        result = imp.data_diffs(rec1, rec2)
        self.assertEqual(result, [])

        # now they're different
        rec2['value'] = 'baz'
        result = imp.data_diffs(rec1, rec2)
        self.assertEqual(result, ['value'])

    def test_normalize_source_data(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)

        # empty source data
        data = imp.normalize_source_data()
        self.assertEqual(data, [])

        # now with 1 record
        setting = model.Setting(name='foo', value='bar')
        data = imp.normalize_source_data(source_objects=[setting])
        self.assertEqual(len(data), 1)
        # nb. default normalizer returns object as-is
        self.assertIs(data[0], setting)

    def test_get_source_objects(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)
        self.assertEqual(imp.get_source_objects(), [])

    def test_normalize_source_object_all(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)
        setting = model.Setting()
        result = imp.normalize_source_object_all(setting)
        self.assertEqual(len(result), 1)
        self.assertIs(result[0], setting)

    def test_normalize_source_object(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)
        setting = model.Setting()
        result = imp.normalize_source_object(setting)
        self.assertIs(result, setting)

    def test_get_target_cache(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)

        with patch.object(imp, 'get_target_objects') as get_target_objects:
            get_target_objects.return_value = []

            # empty cache
            cache = imp.get_target_cache()
            self.assertEqual(cache, {})

            # cache w/ one record
            setting = model.Setting(name='foo', value='bar')
            get_target_objects.return_value = [setting]
            cache = imp.get_target_cache()
            self.assertEqual(len(cache), 1)
            self.assertIn(('foo',), cache)
            foo = cache[('foo',)]
            self.assertEqual(len(foo), 2)
            self.assertEqual(set(foo), {'object', 'data'})
            self.assertIs(foo['object'], setting)
            self.assertEqual(foo['data'], {'name': 'foo', 'value': 'bar'})

    def test_get_target_objects(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)
        self.assertRaises(NotImplementedError, imp.get_target_objects)

    def test_get_target_object(self):
        model = self.app.model
        setting = model.Setting(name='foo', value='bar')

        # nb. must mock up a target cache for this one
        imp = self.make_importer(model_class=model.Setting, caches_target=True)
        imp.cached_target = {
            ('foo',): {
                'object': setting,
                'data': {'name': 'foo', 'value': 'bar'},
            },
        }

        # returns same object
        result = imp.get_target_object(('foo',))
        self.assertIs(result, setting)

        # and one more time just for kicks
        result = imp.get_target_object(('foo',))
        self.assertIs(result, setting)

        # but then not if cache flag is off
        imp.caches_target = False
        result = imp.get_target_object(('foo',))
        self.assertIsNone(result)

    def test_normalize_target_object(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)
        setting = model.Setting(name='foo', value='bar')
        data = imp.normalize_target_object(setting)
        self.assertEqual(data, {'name': 'foo', 'value': 'bar'})

    def test_create_target_object(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)

        # basic
        setting = imp.create_target_object(('foo',), {'name': 'foo', 'value': 'bar'})
        self.assertIsInstance(setting, model.Setting)
        self.assertEqual(setting.name, 'foo')
        self.assertEqual(setting.value, 'bar')

        # will skip if magic delete flag is set
        setting = imp.create_target_object(('foo',), {'name': 'foo', 'value': 'bar',
                                                      '__ignoreme__': True})
        self.assertIsNone(setting)

    def test_make_empty_object(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)
        obj = imp.make_empty_object(('foo',))
        self.assertIsInstance(obj, model.Setting)
        self.assertEqual(obj.name, 'foo')

    def test_make_object(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)
        obj = imp.make_object()
        self.assertIsInstance(obj, model.Setting)

    def test_update_target_object(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)
        setting = model.Setting(name='foo')

        # basic logic for updating *new* object
        obj = imp.update_target_object(setting, {'name': 'foo', 'value': 'bar'})
        self.assertIs(obj, setting)
        self.assertEqual(setting.value, 'bar')


class TestFromFile(DataTestCase):

    def setUp(self):
        self.setup_db()
        self.handler = ImportHandler(self.config)

    def make_importer(self, **kwargs):
        kwargs.setdefault('handler', self.handler)
        return mod.FromFile(self.config, **kwargs)

    def test_setup(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)
        with patch.object(imp, 'open_input_file') as open_input_file:
            imp.setup()
            open_input_file.assert_called_once_with()

    def test_teardown(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)
        with patch.object(imp, 'close_input_file') as close_input_file:
            imp.teardown()
            close_input_file.assert_called_once_with()

    def test_get_input_file_path(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)

        # path is guessed from dir+filename
        path = self.write_file('data.txt', '')
        imp.input_file_dir = self.tempdir
        imp.input_file_name = 'data.txt'
        self.assertEqual(imp.get_input_file_path(), path)

        # path can be explicitly set
        path2 = self.write_file('data2.txt', '')
        imp.input_file_path = path2
        self.assertEqual(imp.get_input_file_path(), path2)

    def test_get_input_file_dir(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)

        # path cannot be guessed
        self.assertRaises(NotImplementedError, imp.get_input_file_dir)

        # path can be explicitly set
        imp.input_file_dir = self.tempdir
        self.assertEqual(imp.get_input_file_dir(), self.tempdir)

    def test_get_input_file_name(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)

        # name cannot be guessed
        self.assertRaises(NotImplementedError, imp.get_input_file_name)

        # name can be explicitly set
        imp.input_file_name = 'data.txt'
        self.assertEqual(imp.get_input_file_name(), 'data.txt')

    def test_open_input_file(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)
        self.assertRaises(NotImplementedError, imp.open_input_file)

    def test_close_input_file(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)

        path = self.write_file('data.txt', '')
        with open(path, 'rt') as f:
            imp.input_file = f
            with patch.object(f, 'close') as close:
                imp.close_input_file()
                close.assert_called_once_with()


class TestToSqlalchemy(DataTestCase):

    def setUp(self):
        self.setup_db()
        self.handler = ImportHandler(self.config)

    def make_importer(self, **kwargs):
        kwargs.setdefault('handler', self.handler)
        return mod.ToSqlalchemy(self.config, **kwargs)

    def test_get_target_object(self):
        model = self.app.model
        setting = model.Setting(name='foo', value='bar')

        # nb. must mock up a target cache for this one
        imp = self.make_importer(model_class=model.Setting, caches_target=True)
        imp.cached_target = {
            ('foo',): {
                'object': setting,
                'data': {'name': 'foo', 'value': 'bar'},
            },
        }

        # returns same object
        result = imp.get_target_object(('foo',))
        self.assertIs(result, setting)

        # and one more time just for kicks
        result = imp.get_target_object(('foo',))
        self.assertIs(result, setting)

        # now let's put a 2nd setting in the db
        setting2 = model.Setting(name='foo2', value='bar2')
        self.session.add(setting2)
        self.session.commit()

        # then we should be able to fetch that via query
        imp.target_session = self.session
        result = imp.get_target_object(('foo2',))
        self.assertIsInstance(result, model.Setting)
        self.assertIs(result, setting2)

        # but sometimes it will not be found
        result = imp.get_target_object(('foo3',))
        self.assertIsNone(result)

    def test_create_target_object(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting, target_session=self.session)
        setting = model.Setting(name='foo', value='bar')

        # new object is added to session
        setting = imp.create_target_object(('foo',), {'name': 'foo', 'value': 'bar'})
        self.assertIsInstance(setting, model.Setting)
        self.assertEqual(setting.name, 'foo')
        self.assertEqual(setting.value, 'bar')
        self.assertIn(setting, self.session)

    def test_get_target_objects(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting, target_session=self.session)

        setting1 = model.Setting(name='foo', value='bar')
        self.session.add(setting1)
        setting2 = model.Setting(name='foo2', value='bar2')
        self.session.add(setting2)
        self.session.commit()

        result = imp.get_target_objects()
        self.assertEqual(len(result), 2)
        self.assertEqual(set(result), {setting1, setting2})
