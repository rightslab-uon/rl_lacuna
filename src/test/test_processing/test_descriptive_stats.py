import unittest
import os
import pandas as pd

from processing.descriptive_stats import DescriptiveStats
from preprocessing.time_split import DayNightSplit, TimeSplit

CURRENT_PATH = os.getcwd()
four_levels_up = os.path.abspath(os.path.join(CURRENT_PATH, '..', '..', '..', '..'))
DATA_PATH = f'{four_levels_up}/Data'
data_file = f'{DATA_PATH}/data_041_280824_020924.csv'
dataframe = pd.read_csv(data_file)

prefixes = ['004', '008', '011']

dataframes = []

for prefix in prefixes:
    data_file = f'{DATA_PATH}/Gurugram/data_{prefix}_020924_090924.csv'
    dataframe = pd.read_csv(data_file)
    sorted_dataframe = dataframe.sort_values(by='data_created_time')
    dataframes.append(sorted_dataframe)

OUTPUT_PATH = f'{four_levels_up}/Coding/outputs'

column_containing_dates = 'data_created_time'


class MyTestCase(unittest.TestCase):
    def test_dataframe(self):
        self.assertIsInstance(dataframe, pd.DataFrame)

    def test_variable_in_dataframe(self):
        column_names = dataframe.columns
        self.assertEqual('pm_25', column_names[4])

    def test_output_dataframe_contains_device_id(self):
        dataframe_of_descriptive_stats = DescriptiveStats([dataframe], ['pm_25']).get_stats()
        column_names = dataframe_of_descriptive_stats.columns
        self.assertEqual('device_id', column_names[1])

    def test_returns_mean_of_first_variable(self):
        dataframe_of_descriptive_stats = DescriptiveStats([dataframe], ['pm_25', 'pm_10']).get_stats()
        mean = dataframe_of_descriptive_stats['mean'].iloc[0]
        self.assertEqual(round(mean, 3), 61.714)

    def test_returns_mean_of_second_variable(self):
        dataframe_of_descriptive_stats = DescriptiveStats([dataframe], ['pm_25', 'pm_10']).get_stats()
        mean = dataframe_of_descriptive_stats['mean'].iloc[1]
        self.assertEqual(round(mean, 3), 83.429)

    def test_output_dataframe_to_csv_in_output_directory(self):
        DescriptiveStats([dataframe], ['pm_25', 'pm_10'], output_directory=OUTPUT_PATH).get_stats()
        self.assertTrue(os.path.exists(f'{OUTPUT_PATH}/descriptive_stats_276_TARA041_groups_1.csv'))

    def test_returns_descriptive_stats_by_two_time_categories(self):
        updated_dataframe = DayNightSplit(dataframe, column_containing_dates, start_of_day=7,
                                          end_of_day=20).split_dataframe()
        dataframe_of_descriptive_stats = DescriptiveStats([updated_dataframe], ['pm_25', 'pm_10'],
                                                          output_directory=OUTPUT_PATH, time_group='group').get_stats()
        mean = dataframe_of_descriptive_stats['mean'].iloc[2]
        self.assertEqual(round(mean, 3), 94.474)

    def test_returns_descriptive_stats_by_several_time_categories(self):
        updated_dataframe = TimeSplit(dataframe, column_containing_dates, 8).split_dataframe()
        dataframe_of_descriptive_stats = DescriptiveStats([updated_dataframe], ['pm_25', 'pm_10'],
                                                          output_directory=OUTPUT_PATH,
                                                          time_group='group_time').get_stats()
        self.assertEqual(len(dataframe_of_descriptive_stats['mean']), 16)

    def test_descriptive_stats_multiple_locations(self):
        dataframe_of_descriptive_stats = DescriptiveStats(dataframes, ['pm_25'],
                                                          output_directory=OUTPUT_PATH).get_stats()
        self.assertEqual(len(dataframe_of_descriptive_stats['mean']), 3)

    def test_descriptive_stats_multiple_locations_multiple_variables(self):
        dataframe_of_descriptive_stats = DescriptiveStats(dataframes, ['pm_25', 'pm_10'],
                                                          output_directory=OUTPUT_PATH).get_stats()
        self.assertEqual(len(dataframe_of_descriptive_stats['mean']), 6)

    def test_descriptive_stats_multiple_locations_multiple_variables_multiple_groups(self):
        updated_dataframes = []
        for frame in dataframes:
            updated_dataframes.append(TimeSplit(frame, column_containing_dates, 8).split_dataframe())
        dataframe_of_descriptive_stats = DescriptiveStats(updated_dataframes, ['pm_25', 'pm_10'],
                                                          output_directory=OUTPUT_PATH,
                                                          time_group='group_time').get_stats()
        self.assertEqual(len(dataframe_of_descriptive_stats['mean']), 48)

    def test_output_dataframe_contains_group_time(self):
        dataframe_of_descriptive_stats = DescriptiveStats([dataframe], ['pm_25']).get_stats()
        self.assertIn('group', dataframe_of_descriptive_stats.columns)


if __name__ == '__main__':
    unittest.main()
