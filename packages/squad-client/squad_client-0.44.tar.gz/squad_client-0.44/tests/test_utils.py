from . import settings
from unittest import TestCase
from unittest.mock import patch
from squad_client.core.api import SquadApi
from squad_client.core.models import Squad, Build
from squad_client.utils import getid, first, get_or_fetch


SquadApi.configure(url='http://localhost:%s' % settings.DEFAULT_SQUAD_PORT)


class UtilsTest(TestCase):
    def setUp(self):
        self.build = first(Squad().builds(version='my_build'))

    def test_getid(self):
        url = 'https://some-squad-url.com/api/objects/42/'
        self.assertEqual(42, getid(url))

    def test_getid_null_url(self):
        self.assertEqual(-1, getid(None))

    def test_getid_not_an_integer(self):
        url = 'https://some-squad-url.com/api/objects/not-an-integer/'
        self.assertEqual(-1, getid(url))

    @patch('squad_client.core.models.Build.__fetch__')
    def test_get_or_fetch(self, fetch_mock):
        get_or_fetch(Build, self.build.id)
        fetch_mock.assert_called()

        fetch_mock.reset_mock()

        get_or_fetch(Build, self.build.id)
        fetch_mock.assert_not_called()
