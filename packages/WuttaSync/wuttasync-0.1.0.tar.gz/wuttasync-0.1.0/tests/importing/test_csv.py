#-*- coding: utf-8; -*-

import csv
from unittest.mock import patch

from wuttjamaican.testing import DataTestCase

from wuttasync.importing import csv as mod, ImportHandler, ToSqlalchemyHandler, ToSqlalchemy


class TestFromCsv(DataTestCase):

    def setUp(self):
        self.setup_db()
        self.handler = ImportHandler(self.config)

    def make_importer(self, **kwargs):
        kwargs.setdefault('handler', self.handler)
        return mod.FromCsv(self.config, **kwargs)

    def test_get_input_file_name(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)

        # name can be guessed
        self.assertEqual(imp.get_input_file_name(), 'Setting.csv')

        # name can be explicitly set
        imp.input_file_name = 'data.txt'
        self.assertEqual(imp.get_input_file_name(), 'data.txt')

    def test_open_input_file(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)

        path = self.write_file('data.txt', '')
        imp.input_file_path = path
        imp.open_input_file()
        self.assertEqual(imp.input_file.name, path)
        self.assertIsInstance(imp.input_reader, csv.DictReader)
        imp.input_file.close()

    def test_close_input_file(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)

        path = self.write_file('data.txt', '')
        imp.input_file_path = path
        imp.open_input_file()
        imp.close_input_file()
        self.assertFalse(hasattr(imp, 'input_reader'))
        self.assertFalse(hasattr(imp, 'input_file'))

    def test_get_source_objects(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)

        path = self.write_file('data.csv', """\
name,value
foo,bar
foo2,bar2
""")
        imp.input_file_path = path
        imp.open_input_file()
        objects = imp.get_source_objects()
        imp.close_input_file()
        self.assertEqual(len(objects), 2)
        self.assertEqual(objects[0], {'name': 'foo', 'value': 'bar'})
        self.assertEqual(objects[1], {'name': 'foo2', 'value': 'bar2'})


class MockMixinHandler(mod.FromCsvToSqlalchemyMixin, ToSqlalchemyHandler):
    ToImporterBase = ToSqlalchemy


class TestFromCsvToSqlalchemyMixin(DataTestCase):

    def make_handler(self, **kwargs):
        return MockMixinHandler(self.config, **kwargs)

    def test_get_target_model(self):
        with patch.object(mod.FromCsvToSqlalchemyMixin, 'define_importers', return_value={}):
            handler = self.make_handler()
            self.assertRaises(NotImplementedError, handler.get_target_model)

    def test_define_importers(self):
        model = self.app.model
        with patch.object(mod.FromCsvToSqlalchemyMixin, 'get_target_model', return_value=model):
            handler = self.make_handler()
            importers = handler.define_importers()
            self.assertIn('Setting', importers)
            self.assertTrue(issubclass(importers['Setting'], mod.FromCsv))
            self.assertTrue(issubclass(importers['Setting'], ToSqlalchemy))
            self.assertIn('User', importers)
            self.assertIn('Person', importers)
            self.assertIn('Role', importers)

    def test_make_importer_factory(self):
        model = self.app.model
        with patch.object(mod.FromCsvToSqlalchemyMixin, 'define_importers', return_value={}):
            handler = self.make_handler()
            factory = handler.make_importer_factory(model.Setting, 'Setting')
            self.assertTrue(issubclass(factory, mod.FromCsv))
            self.assertTrue(issubclass(factory, ToSqlalchemy))


class TestFromCsvToWutta(DataTestCase):

    def make_handler(self, **kwargs):
        return mod.FromCsvToWutta(self.config, **kwargs)

    def test_get_target_model(self):
        handler = self.make_handler()
        self.assertIs(handler.get_target_model(), self.app.model)
