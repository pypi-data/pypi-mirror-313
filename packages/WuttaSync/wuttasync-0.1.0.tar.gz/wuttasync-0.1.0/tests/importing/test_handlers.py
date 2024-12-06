#-*- coding: utf-8; -*-

from collections import OrderedDict
from unittest.mock import patch

from wuttjamaican.testing import DataTestCase

from wuttasync.importing import handlers as mod, Importer, ToSqlalchemy


class TestImportHandler(DataTestCase):

    def make_handler(self, **kwargs):
        return mod.ImportHandler(self.config, **kwargs)

    def test_str(self):
        handler = self.make_handler()
        self.assertEqual(str(handler), "None → None")

        handler.source_title = 'CSV'
        handler.target_title = 'Wutta'
        self.assertEqual(str(handler), "CSV → Wutta")

    def test_actioning(self):
        handler = self.make_handler()
        self.assertEqual(handler.actioning, 'importing')

        handler.orientation = mod.Orientation.EXPORT
        self.assertEqual(handler.actioning, 'exporting')

    def test_get_key(self):
        handler = self.make_handler()
        self.assertEqual(handler.get_key(), 'to_None.from_None.import')

        with patch.multiple(mod.ImportHandler, source_key='csv', target_key='wutta'):
            self.assertEqual(handler.get_key(), 'to_wutta.from_csv.import')

    def test_get_spec(self):
        handler = self.make_handler()
        self.assertEqual(handler.get_spec(), 'wuttasync.importing.handlers:ImportHandler')

    def test_get_title(self):
        handler = self.make_handler()
        self.assertEqual(handler.get_title(), "None → None")

        handler.source_title = 'CSV'
        handler.target_title = 'Wutta'
        self.assertEqual(handler.get_title(), "CSV → Wutta")

    def test_get_source_title(self):
        handler = self.make_handler()

        # null by default
        self.assertIsNone(handler.get_source_title())

        # which is really using source_key as fallback
        handler.source_key = 'csv'
        self.assertEqual(handler.get_source_title(), 'csv')

        # can also use (defined) generic fallback
        handler.generic_source_title = 'CSV'
        self.assertEqual(handler.get_source_title(), 'CSV')

        # or can set explicitly
        handler.source_title = 'XXX'
        self.assertEqual(handler.get_source_title(), 'XXX')

    def test_get_target_title(self):
        handler = self.make_handler()

        # null by default
        self.assertIsNone(handler.get_target_title())

        # which is really using target_key as fallback
        handler.target_key = 'wutta'
        self.assertEqual(handler.get_target_title(), 'wutta')

        # can also use (defined) generic fallback
        handler.generic_target_title = 'Wutta'
        self.assertEqual(handler.get_target_title(), 'Wutta')

        # or can set explicitly
        handler.target_title = 'XXX'
        self.assertEqual(handler.get_target_title(), 'XXX')

    def test_process_data(self):
        model = self.app.model
        handler = self.make_handler()

        # empy/no-op should commit (not fail)
        with patch.object(handler, 'commit_transaction') as commit_transaction:
            handler.process_data()
            commit_transaction.assert_called_once_with()

        # do that again with no patch, just for kicks
        handler.process_data()

        # dry-run should rollback
        with patch.object(handler, 'commit_transaction') as commit_transaction:
            with patch.object(handler, 'rollback_transaction') as rollback_transaction:
                handler.process_data(dry_run=True)
                self.assertFalse(commit_transaction.called)
                rollback_transaction.assert_called_once_with()

        # and do that with no patch, for kicks
        handler.process_data(dry_run=True)

        # outright error should cause rollback
        with patch.object(handler, 'commit_transaction') as commit_transaction:
            with patch.object(handler, 'rollback_transaction') as rollback_transaction:
                with patch.object(handler, 'get_importer', side_effect=RuntimeError):
                    self.assertRaises(RuntimeError, handler.process_data, 'BlahBlah')
                    self.assertFalse(commit_transaction.called)
                    rollback_transaction.assert_called_once_with()

        # fake importer class/data
        mock_source_objects = [{'name': 'foo', 'value': 'bar'}]
        class SettingImporter(ToSqlalchemy):
            model_class = model.Setting
            target_session = self.session
            def get_source_objects(self):
                return mock_source_objects

        # now for a "normal" one
        handler.importers['Setting'] = SettingImporter
        self.assertEqual(self.session.query(model.Setting).count(), 0)
        handler.process_data('Setting')
        self.assertEqual(self.session.query(model.Setting).count(), 1)

        # then add another mock record
        mock_source_objects.append({'name': 'foo2', 'value': 'bar2'})
        handler.process_data('Setting')
        self.assertEqual(self.session.query(model.Setting).count(), 2)

        # nb. even if dry-run, record is added
        # (rollback would happen later in that case)
        mock_source_objects.append({'name': 'foo3', 'value': 'bar3'})
        handler.process_data('Setting', dry_run=True)
        self.assertEqual(self.session.query(model.Setting).count(), 3)

    def test_consume_kwargs(self):
        handler = self.make_handler()

        # kwargs are returned as-is
        kw = {}
        result = handler.consume_kwargs(kw)
        self.assertIs(result, kw)

        # captures dry-run flag
        self.assertFalse(handler.dry_run)
        kw['dry_run'] = True
        result = handler.consume_kwargs(kw)
        self.assertIs(result, kw)
        self.assertTrue(kw['dry_run'])
        self.assertTrue(handler.dry_run)

    def test_define_importers(self):
        handler = self.make_handler()
        importers = handler.define_importers()
        self.assertEqual(importers, {})
        self.assertIsInstance(importers, OrderedDict)

    def test_get_importer(self):
        model = self.app.model
        handler = self.make_handler()

        # normal
        handler.importers['Setting'] = Importer
        importer = handler.get_importer('Setting', model_class=model.Setting)
        self.assertIsInstance(importer, Importer)

        # key not found
        self.assertRaises(KeyError, handler.get_importer, 'BunchOfNonsense', model_class=model.Setting)


class TestToSqlalchemyHandler(DataTestCase):

    def make_handler(self, **kwargs):
        return mod.ToSqlalchemyHandler(self.config, **kwargs)

    def test_begin_target_transaction(self):
        handler = self.make_handler()
        with patch.object(handler, 'make_target_session') as make_target_session:
            make_target_session.return_value = self.session
            self.assertIsNone(handler.target_session)
            handler.begin_target_transaction()
            make_target_session.assert_called_once_with()

    def test_rollback_target_transaction(self):
        handler = self.make_handler()
        with patch.object(handler, 'make_target_session') as make_target_session:
            make_target_session.return_value = self.session
            self.assertIsNone(handler.target_session)
            handler.begin_target_transaction()
            self.assertIs(handler.target_session, self.session)
            handler.rollback_target_transaction()
            self.assertIsNone(handler.target_session)

    def test_commit_target_transaction(self):
        handler = self.make_handler()
        with patch.object(handler, 'make_target_session') as make_target_session:
            make_target_session.return_value = self.session
            self.assertIsNone(handler.target_session)
            handler.begin_target_transaction()
            self.assertIs(handler.target_session, self.session)
            handler.commit_target_transaction()
            self.assertIsNone(handler.target_session)

    def test_make_target_session(self):
        handler = self.make_handler()
        self.assertRaises(NotImplementedError, handler.make_target_session)

    def test_get_importer_kwargs(self):
        handler = self.make_handler()
        handler.target_session = self.session
        kw = handler.get_importer_kwargs('Setting')
        self.assertIn('target_session', kw)
        self.assertIs(kw['target_session'], self.session)
