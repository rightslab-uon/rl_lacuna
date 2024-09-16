import unittest

from processing import Formatting


class MyTestCase(unittest.TestCase):
    def test_format_string(self):
        initial_string = 'hello_world'
        new_string = Formatting.format_string(initial_string)
        self.assertEqual(new_string, 'Hello World')

    def test_units(self):
        pollutant = 'pm_10'
        units = Formatting.get_units(pollutant)
        self.assertEqual(units, 'μm/m³')

    def test_get_pollutant_name(self):
        pollutant = 'no2'
        name = Formatting.get_pollutant_name(pollutant)
        self.assertEqual(name, 'NO\u2082')

    def test_get_pollutant_name_if_other(self):
        pollutant = 'mean'
        name = Formatting.get_pollutant_name(pollutant)
        self.assertEqual(name, 'Mean')


if __name__ == '__main__':
    unittest.main()
