import os
import time
import unittest
from lumipy.provider.factory import Factory
from lumipy.test.test_infra import get_logs
from pathlib import Path
import tempfile


class TestProviderFactory(unittest.TestCase):

    def test_provider_factory_ctor_happy(self):
        fact = Factory(
            host='localhost',
            port=5464,
            user='TESTUSER',
            domain='test-domain',
            whitelist_me=True,
            _skip_checks=True,
            _fbn_run=False,
        )

        self.assertEqual('test-domain', fact.domain)
        self.assertFalse(fact.errored)
        self.assertIsNone(fact.process)
        self.assertTrue(fact.starting)

        self.assertIn('--authClientDomain=test-domain', fact.cmd)
        self.assertIn('--localRoutingUserId "TESTUSER"', fact.cmd)
        self.assertIn('--config "PythonProvider:BaseUrl=>http://localhost:5464/api/v1/"', fact.cmd)

    def test_provider_factory_ctor_happy_global(self):
        fact = Factory(
            host='localhost',
            port=5464,
            user='global',
            domain='test-domain',
            whitelist_me=True,
            _skip_checks=True,
            _fbn_run=False,
        )

        self.assertEqual('test-domain', fact.domain)
        self.assertFalse(fact.errored)
        self.assertIsNone(fact.process)
        self.assertTrue(fact.starting)

        # It is important that --routeAs:Global comes before --config
        dll_path = Path(tempfile.gettempdir()) / 'test' / 'path' / 'Finbourne.Honeycomb.Host.dll'

        self.assertIn(
            f'dotnet {dll_path} --quiet --authClientDomain=test-domain '
            '--routeAs:Global --config "PythonProvider:BaseUrl=>http://localhost:5464/api/v1/" '
            '"DataProvider:RoutingTypeGlobalMachineWhitelist=>', fact.cmd)

    def test_provider_factory_ctor_happy_via_proxy(self):
        fact = Factory(
            host='localhost',
            port=5464,
            user='global',
            domain='test-domain',
            whitelist_me=True,
            _skip_checks=True,
            _fbn_run=False,
            via_proxy=True,
        )

        self.assertEqual('test-domain', fact.domain)
        self.assertFalse(fact.errored)
        self.assertIsNone(fact.process)
        self.assertTrue(fact.starting)

        dll_path = Path(tempfile.gettempdir()) / 'test' / 'path' / 'Finbourne.Honeycomb.Host.dll'

        self.assertIn('--viaProxy ', fact.cmd)

    def test_provider_factory_ctor_unhappy(self):
        with self.assertRaises(ValueError):
            Factory(host='$(bad stuff)', port=1234, user='user', domain='dom', whitelist_me=False, _fbn_run=False)

        with self.assertRaises(ValueError):
            Factory(host='127.0.0.1', port="ABC", user='user', domain='dom', whitelist_me=False, _fbn_run=False)

    def test_factory_logs_with_valid_command(self):
        stdout, stderr = get_logs(func=self.wrapper_get_factory_logs_happy)

        self.assertFalse(stderr)
        self.assertIn("hello_from_a_test_hello_from_a_test_", stdout)

    def test_factory_logs_with_unhappy_command(self):
        stdout, stderr = get_logs(func=self.wrapper_get_factory_logs_unhappy)

        # We have no stderr here because we log any stderr to the stdout
        self.assertFalse(stderr)
        self.assertIn("This is a message to stderr", stdout)

    def wrapper_get_factory_logs_unhappy(self):
        return self.get_factory_logs(cmd="python -c import sys; sys.stderr.write('This is a message to stderr')")

    def wrapper_get_factory_logs_happy(self):
        return self.get_factory_logs(cmd="python -c print('hello_from_a_test_'*2)")

    @staticmethod
    def get_factory_logs(cmd):
        fact = Factory(
            host='localhost',
            port=5464,
            user='global',
            domain='test-domain',
            whitelist_me=True,
            _skip_checks=True,
            _fbn_run=False,
        )

        fact.cmd = cmd
        fact.start()

        while fact.process.poll() is None:
            time.sleep(0.1)

        fact.process.stdout.close()
        fact.process.stderr.close()
