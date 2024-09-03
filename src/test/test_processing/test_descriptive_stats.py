import unittest
import os
import pandas as pd

from processing.descriptive_stats import DescriptiveStats

CURRENT_PATH = os.getcwd()
four_levels_up = os.path.abspath(os.path.join(CURRENT_PATH, '..', '..', '..', '..'))
DATA_PATH = f'{four_levels_up}/Data'
data_file = f'{DATA_PATH}/data_041_280824_020924.csv'
dataframe = pd.read_csv(data_file)

OUTPUT_PATH = f'{four_levels_up}/Coding/outputs'

class MyTestCase(unittest.TestCase):
    def test_dataframe(self):
        self.assertTrue(isinstance(dataframe, pd.DataFrame))

    def test_variable_in_dataframe(self):
        column_names = dataframe.columns
        self.assertEqual('pm_25', column_names[4])

    def test_output_dataframe_contains_device_id(self):
        dataframe_of_descriptive_stats = DescriptiveStats(dataframe, ['pm_25']).get_stats()
        column_names = dataframe_of_descriptive_stats.columns
        self.assertEqual('device_id', column_names[1])
    def test_returns_mean_of_first_variable(self):
        dataframe_of_descriptive_stats = DescriptiveStats(dataframe, ['pm_25', 'pm_10']).get_stats()
        mean = dataframe_of_descriptive_stats['mean'].iloc[0]
        self.assertEqual(round(mean,3), 60.227)

    def test_returns_mean_of_second_variable(self):
        dataframe_of_descriptive_stats = DescriptiveStats(dataframe, ['pm_25', 'pm_10']).get_stats()
        mean = dataframe_of_descriptive_stats['mean'].iloc[1]
        self.assertEqual(round(mean, 3), 87.447)

    def test_output_dataframe_to_csv_in_output_directory(self):
        DescriptiveStats(dataframe, ['pm_25', 'pm_10'], output_directory=OUTPUT_PATH).get_stats()
        self.assertTrue(os.path.exists(f'{OUTPUT_PATH}/descriptive_stats_276_TARA041.csv'))

if __name__ == '__main__':
    unittest.main()
