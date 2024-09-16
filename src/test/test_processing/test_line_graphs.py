import unittest
import os
import pandas as pd

from processing.line_graphs import LineGraphs

CURRENT_PATH = os.getcwd()
four_levels_up = os.path.abspath(os.path.join(CURRENT_PATH, '..', '..', '..', '..'))
DATA_PATH = f'{four_levels_up}/Data'
data_file = f'{DATA_PATH}/data_041_280824_020924.csv'
data_file_second_location = f'{DATA_PATH}/data_062_260824_020924.csv'
dataframe = pd.read_csv(data_file)
dataframe_second_location = pd.read_csv(data_file_second_location)

OUTPUT_PATH = f'{four_levels_up}/Coding/outputs'

column_containing_dates = 'data_created_time'


class MyTestCase(unittest.TestCase):
    def test_saved_line_graph_two_variables_same_location(self):
        LineGraphs(dataframe, ['pm_25', 'pm_10'], 'data_created_time', output_directory=OUTPUT_PATH).line_plot()
        self.assertTrue(os.path.exists(f'{OUTPUT_PATH}/Line_Plot_data_created_time_pm_25_pm_10_at_276_TARA041.png'))

    def test_saved_line_graph_two_locations(self):
        # Adding prefix to column names
        df1_prefixed = dataframe.add_prefix('041_')
        df2_prefixed = dataframe_second_location.add_prefix('062_')
        # Renaming the 'ID' column back to its original name for merging
        df1_prefixed = df1_prefixed.rename(columns={'041_data_created_time': 'data_created_time'})
        df2_prefixed = df2_prefixed.rename(columns={'062_data_created_time': 'data_created_time'})
        # Merging DataFrames on 'data_created_time' column - need to do with the one that started earlier first
        merged_dataframe = pd.merge(df2_prefixed, df1_prefixed, on='data_created_time', how='outer')
        LineGraphs(merged_dataframe, ['041_pm_25', '062_pm_25'], 'data_created_time', locations='041_062',
                   output_directory=OUTPUT_PATH).line_plot()
        self.assertTrue(os.path.exists(f'{OUTPUT_PATH}/Line_Plot_data_created_time_at_041_062.png'))

    def test_saved_line_graph_two_locations_date_time_column(self):
        # Adding prefix to column names
        df1_prefixed = dataframe.add_prefix('041_')
        df2_prefixed = dataframe_second_location.add_prefix('062_')
        # Renaming the 'ID' column back to its original name for merging
        df1_prefixed = df1_prefixed.rename(columns={'041_data_created_time': 'data_created_time'})
        df2_prefixed = df2_prefixed.rename(columns={'062_data_created_time': 'data_created_time'})
        # Merging DataFrames on 'data_created_time' column - need to do with the one that started earlier first
        merged_dataframe = pd.merge(df2_prefixed, df1_prefixed, on='data_created_time', how='outer')
        merged_dataframe['data_created_time'] = pd.to_datetime(merged_dataframe['data_created_time'])
        LineGraphs(merged_dataframe, ['041_pm_25', '062_pm_25'], 'data_created_time', locations='041_062_time',
                   output_directory=OUTPUT_PATH).line_plot()
        self.assertTrue(os.path.exists(f'{OUTPUT_PATH}/Line_Plot_data_created_time_at_041_062_time.png'))


if __name__ == '__main__':
    unittest.main()
