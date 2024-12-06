#-*- coding: utf-8; -*-

from unittest.mock import patch

from wuttjamaican.testing import DataTestCase

from wuttasync.importing import wutta as mod


class TestToWuttaHandler(DataTestCase):

    def make_handler(self, **kwargs):
        return mod.ToWuttaHandler(self.config, **kwargs)

    def test_get_target_title(self):
        handler = self.make_handler()

        # uses app title by default
        self.config.setdefault('wutta.app_title', "What About This")
        self.assertEqual(handler.get_target_title(), 'What About This')

        # or generic default if present
        handler.generic_target_title = "WHATABOUTTHIS"
        self.assertEqual(handler.get_target_title(), 'WHATABOUTTHIS')

        # but prefer specific title if present
        handler.target_title = "what_about_this"
        self.assertEqual(handler.get_target_title(), 'what_about_this')

    def test_make_target_session(self):
        handler = self.make_handler()

        # makes "new" (mocked in our case) app session
        with patch.object(self.app, 'make_session') as make_session:
            make_session.return_value = self.session
            session = handler.make_target_session()
            make_session.assert_called_once_with()
            self.assertIs(session, self.session)
