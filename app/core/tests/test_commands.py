from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    @patch('django.db.utils.ConnectionHandler.__getitem__')
    def test_wait_for_db_ready(self, gi):
        gi.return_value = True
        call_command('wait_for_db')

        self.assertEqual(gi.call_count, 1)

    @patch('django.db.utils.ConnectionHandler.__getitem__')
    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts, gi):
        gi.side_effect = [OperationalError] * 5 + [True]
        call_command('wait_for_db')

        self.assertEqual(gi.call_count, 6)
