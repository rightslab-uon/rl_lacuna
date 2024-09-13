import unittest
import os
import pandas as pd

from processing.time_split import TimeSplit, DayNightSplit

CURRENT_PATH = os.getcwd()
four_levels_up = os.path.abspath(os.path.join(CURRENT_PATH, '..', '..', '..', '..'))
DATA_PATH = f'{four_levels_up}/Data'
data_file = f'{DATA_PATH}/data_041_280824_020924.csv'
dataframe = pd.read_csv(data_file)

column_containing_dates = 'data_created_time'

class MyTestCase(unittest.TestCase):
    def test_date_time_column_split(self):
        updated_dataframe = TimeSplit(dataframe, column_containing_dates).split_dataframe()
        column_names = updated_dataframe.columns
        self.assertEqual('date', column_names[15])

    def test_day_of_week_time_column_split(self):
        updated_dataframe = TimeSplit(dataframe, column_containing_dates).split_dataframe()
        column_names = updated_dataframe.columns
        self.assertEqual('day_of_week', column_names[17])

    def test_time_split_grouping_8_groups_3_hours(self):
        updated_dataframe = TimeSplit(dataframe, column_containing_dates, 8).split_dataframe()
        group = updated_dataframe['group'].iloc[0]
        self.assertEqual(group, 3)

    def test_time_split_grouping_8_groups_3_hours_with_group_time(self):
        updated_dataframe = TimeSplit(dataframe, column_containing_dates, 8).split_dataframe()
        group_time = updated_dataframe['group_time'].iloc[0]
        self.assertEqual(group_time, '09:00-12:00')

    def test_time_split_grouping_2_groups_12_hours(self):
        updated_dataframe = TimeSplit(dataframe, column_containing_dates, 2).split_dataframe()
        group = updated_dataframe['group'].iloc[0]
        self.assertEqual(group, 0)

    def test_night_day_grouping(self):
        updated_dataframe = DayNightSplit(dataframe, column_containing_dates, start_of_day=7, end_of_day=20).split_dataframe()
        number_groups = updated_dataframe['group'].nunique()
        self.assertEqual(number_groups, 2)


if __name__ == '__main__':
    unittest.main()
