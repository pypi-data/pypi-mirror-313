import unittest
from lumipy.provider.common import strtobool


class TestStrToBool(unittest.TestCase):

    base_true_values = ['y', 'yes', 't', 'true', 'on', '1']
    base_false_values = ['n', 'no', 'f', 'false', 'off', '0']
    invalid_values = ['problematic', '2', '']

    true_values = base_true_values + [val.upper() for val in base_true_values]
    false_values = base_false_values + [val.upper() for val in base_false_values]

    def test_strtobool_true(self):
        for val in self.true_values:
            self.assertTrue(strtobool(val))

    def test_strtobool_false(self):
        for val in self.false_values:
            self.assertFalse(strtobool(val))

    def test_strtobool_invalid_args(self):
        for val in self.invalid_values:
            with self.assertRaises(ValueError):
                strtobool(val)
