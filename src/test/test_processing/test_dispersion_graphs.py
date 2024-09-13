import unittest
import os
import pandas as pd

from processing.descriptive_stats import DescriptiveStats
from processing.dispersion_graphs import DispersionGraph
from processing.time_split import TimeSplit

CURRENT_PATH = os.getcwd()
four_levels_up = os.path.abspath(os.path.join(CURRENT_PATH, '..', '..', '..', '..'))
DATA_PATH = f'{four_levels_up}/Data'
data_file = f'{DATA_PATH}/data_041_280824_020924.csv'
data_file_second_location = f'{DATA_PATH}/data_062_260824_020924.csv'
dataframe = pd.read_csv(data_file)
dataframe_second_location = pd.read_csv(data_file_second_location)

data_file = f'{DATA_PATH}/data_041_280824_020924.csv'

prefixes = ['004', '008', '011']

dataframes = []

for prefix in prefixes:
    data_file = f'{DATA_PATH}/Gurugram/data_{prefix}_020924_090924.csv'
    dataframe = pd.read_csv(data_file)
    sorted_dataframe = dataframe.sort_values(by='data_created_time')
    dataframes.append(sorted_dataframe)

# Adding prefix to column names
df1_prefixed = dataframe.add_prefix('041_')
df2_prefixed = dataframe_second_location.add_prefix('062_')
# Renaming the 'ID' column back to its original name for merging
df1_prefixed = df1_prefixed.rename(columns={'041_data_created_time': 'data_created_time'})
df2_prefixed = df2_prefixed.rename(columns={'062_data_created_time': 'data_created_time'})

prefixed_dataframes = [df1_prefixed, df2_prefixed]

merged_dataframe = prefixed_dataframes[0]
# Iterate and merge
for frame in prefixed_dataframes[1:]:
    merged_dataframe = merged_dataframe.merge(frame, on='data_created_time', how='outer')

OUTPUT_PATH = f'{four_levels_up}/Coding/outputs'

column_containing_dates = 'data_created_time'

class MyTestCase(unittest.TestCase):
    def test_all_data_by_hour_dispersion_plot_one_variable(self):
        updated_dataframe = TimeSplit(dataframe, column_containing_dates, 8).split_dataframe()
        DispersionGraph(updated_dataframe, ['pm_25'], 'hour', output_directory=OUTPUT_PATH).dispersion_graph()
        self.assertTrue(os.path.exists(f'{OUTPUT_PATH}/Dispersion_Plot_hour_at_276_TARA041.png'))

    def test_all_data_by_day_dispersion_plot_one_variable(self):
        updated_dataframe = TimeSplit(dataframe, column_containing_dates, 8).split_dataframe()
        DispersionGraph(updated_dataframe, ['pm_25'], 'date', output_directory=OUTPUT_PATH).dispersion_graph()
        self.assertTrue(os.path.exists(f'{OUTPUT_PATH}/Dispersion_Plot_date_at_276_TARA041.png'))

    def test_means_data_by_hour_one_variable_multiple_sites(self):
        updated_dataframe = TimeSplit(merged_dataframe, column_containing_dates, 8).split_dataframe()
        DispersionGraph(updated_dataframe, ['041_pm_25', '062_pm_25'], 'hour', locations_stat_variable='041_062', output_directory=OUTPUT_PATH).dispersion_graph()
        self.assertTrue(os.path.exists(f'{OUTPUT_PATH}/Dispersion_Plot_hour_at_041_062.png'))

    def test_means_data_by_date_one_variable_multiple_sites(self):
        updated_dataframe = TimeSplit(merged_dataframe, column_containing_dates, 8).split_dataframe()
        DispersionGraph(updated_dataframe, ['041_pm_25', '062_pm_25'], 'date', locations_stat_variable='041_062', output_directory=OUTPUT_PATH).dispersion_graph()
        self.assertTrue(os.path.exists(f'{OUTPUT_PATH}/Dispersion_Plot_date_at_041_062.png'))

    def test_means_data_multiple_locations_by_group(self):
        updated_dataframes = []
        for frame in dataframes:
            updated_dataframes.append(TimeSplit(frame, column_containing_dates, 8).split_dataframe())
        dataframe_of_descriptive_stats = DescriptiveStats(updated_dataframes, ['pm_25', 'pm_10'],
                                                          time_group='group_time').get_stats()
        focused_dataframe = dataframe_of_descriptive_stats[dataframe_of_descriptive_stats['variable'] == 'pm_25']
        DispersionGraph(focused_dataframe, ['mean'], 'group_time', locations_stat_variable='004_008_011_mean_pm_25', output_directory=OUTPUT_PATH).dispersion_graph()
        self.assertTrue(os.path.exists(f'{OUTPUT_PATH}/Dispersion_Plot_group_time_at_004_008_011.png'))


if __name__ == '__main__':
    unittest.main()
