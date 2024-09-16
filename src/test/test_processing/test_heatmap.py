import unittest
import os
import pandas as pd

from processing.descriptive_stats import DescriptiveStats
from preprocessing.time_split import TimeSplit
from processing.heatmap import Heatmap


CURRENT_PATH = os.getcwd()
four_levels_up = os.path.abspath(os.path.join(CURRENT_PATH, '..', '..', '..', '..'))
DATA_PATH = f'{four_levels_up}/Data'
data_file = f'{DATA_PATH}/data_041_280824_020924.csv'
data_file_second_location = f'{DATA_PATH}/data_062_260824_020924.csv'

dataframe = pd.read_csv(data_file)
dataframe_second_location = pd.read_csv(data_file_second_location)

OUTPUT_PATH = f'{four_levels_up}/Coding/outputs'

column_containing_dates = 'data_created_time'

# Combine two datasets with different locations
# Adding prefix to column names
df1_prefixed = dataframe.add_prefix('041_')
df2_prefixed = dataframe_second_location.add_prefix('062_')
# Renaming the 'ID' column back to its original name for merging
df1_prefixed = df1_prefixed.rename(columns={'041_data_created_time': 'data_created_time'})
df2_prefixed = df2_prefixed.rename(columns={'062_data_created_time': 'data_created_time'})
# Merging DataFrames on 'data_created_time' column - need to do with the one that started earlier first
merged_dataframe = pd.merge(df2_prefixed, df1_prefixed, on='data_created_time', how='outer')


class MyTestCase(unittest.TestCase):
    def test_heatmap(self):
        dataframes = [dataframe, dataframe_second_location]
        updated_dataframes = []
        for df in dataframes:
            updated_dataframe = TimeSplit(df, column_containing_dates, 8).split_dataframe()
            updated_dataframes.append(updated_dataframe.sort_values('group_time'))
        dataframe_of_descriptive_stats = DescriptiveStats(updated_dataframes, ['pm_25', 'pm_10'],
                                                          time_group='group_time').get_stats()
        focused_dataframe = dataframe_of_descriptive_stats[dataframe_of_descriptive_stats['variable'] == 'pm_25']
        Heatmap(focused_dataframe, 'mean', 'device_id', 'group_time', '041_062_pm_25', output_directory=OUTPUT_PATH).heatmap_plot()
        self.assertTrue(os.path.exists(f'{OUTPUT_PATH}/Heatmap_device_id_mean_at_041_062_pm_25.png'))


if __name__ == '__main__':
    unittest.main()
