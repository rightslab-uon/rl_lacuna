import unittest
import os
import pandas as pd

from processing.box_whisker_graphs import BoxWhiskerGraph, MeltDataframe
from processing.clean_data import CleanData
from processing.time_split import TimeSplit


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
    def test_by_hour_box_whisker_plot_one_variable_hour(self):
        updated_dataframe = TimeSplit(dataframe, column_containing_dates, 8).split_dataframe()
        BoxWhiskerGraph(updated_dataframe, 'pm_25', 'hour', output_directory=OUTPUT_PATH).box_whisker_graph()
        self.assertTrue(os.path.exists(f'{OUTPUT_PATH}/Box_Whisker_Plot_hour_at_276_TARA041.png'))

    def test_by_date_box_whisker_plot_one_variable_date(self):
        updated_dataframe = TimeSplit(dataframe, column_containing_dates, 8).split_dataframe()
        BoxWhiskerGraph(updated_dataframe, 'pm_25', 'date', output_directory=OUTPUT_PATH).box_whisker_graph()
        self.assertTrue(os.path.exists(f'{OUTPUT_PATH}/Box_Whisker_Plot_date_at_276_TARA041.png'))

    def test_by_day_of_week_box_whisker_plot_one_variable_day_of_week(self):
        updated_dataframe = TimeSplit(dataframe, column_containing_dates, 8).split_dataframe()
        BoxWhiskerGraph(updated_dataframe, 'pm_25', 'day_of_week', output_directory=OUTPUT_PATH).box_whisker_graph()
        self.assertTrue(os.path.exists(f'{OUTPUT_PATH}/Box_Whisker_Plot_day_of_week_at_276_TARA041.png'))

    def test_by_location_one_variable_multiple_sites(self):
        updated_dataframe = TimeSplit(merged_dataframe, column_containing_dates, 8).split_dataframe()
        # Prepare data so it can be used in box and whisker
        df_melted = MeltDataframe(updated_dataframe, 'locations', 'pm_25', 'day_of_week', ['062_pm_25', '041_pm_25'],
                                  location_more_than_one=True).get_melted_dataframe()
        BoxWhiskerGraph(df_melted, 'pm_25', 'day_of_week', multiple='locations', locations='041_062', output_directory=OUTPUT_PATH).box_whisker_graph()

        self.assertTrue(os.path.exists(f'{OUTPUT_PATH}/Box_Whisker_Plot_day_of_week_at_041_062.png'))

    def test_by_location_one_variable_grouped_hours_multiple_sites(self):
        updated_dataframe = TimeSplit(merged_dataframe, column_containing_dates, 8).split_dataframe()
        # Prepare data so it can be used in box and whisker
        df_melted = MeltDataframe(updated_dataframe, 'locations', 'pm_25', 'group', ['062_pm_25', '041_pm_25'],
                                  location_more_than_one=True).get_melted_dataframe()
        BoxWhiskerGraph(df_melted, 'pm_25', 'group', multiple='locations', locations='041_062', output_directory=OUTPUT_PATH).box_whisker_graph()

        self.assertTrue(os.path.exists(f'{OUTPUT_PATH}/Box_Whisker_Plot_group_at_041_062.png'))

    def test_multiple_sites_multiple_variables(self):
        updated_dataframe = TimeSplit(merged_dataframe, column_containing_dates, 1).split_dataframe()
        focused_dataframe = updated_dataframe[['062_pm_25', '041_pm_25', '062_pm_10', '041_pm_10', '062_no2', '041_no2']]
        df_melted = focused_dataframe.melt(var_name='Pollutant', value_name='value')
        BoxWhiskerGraph(df_melted, 'value', 'Pollutant', locations='041_062_range_pollutants',
                        output_directory=OUTPUT_PATH).box_whisker_graph()
        self.assertTrue(os.path.exists(f'{OUTPUT_PATH}/Box_Whisker_Plot_Pollutant_at_041_062_range_pollutants.png'))

    def test_multiple_sites_one_variable(self):
        updated_dataframe = TimeSplit(merged_dataframe, column_containing_dates, 1).split_dataframe()
        focused_dataframe = updated_dataframe[['062_pm_25', '041_pm_25']]
        df_melted = focused_dataframe.melt(var_name='Pollutant', value_name='value')
        BoxWhiskerGraph(df_melted, 'value', 'Pollutant', locations='041_062_pm_25',
                        output_directory=OUTPUT_PATH).box_whisker_graph()
        self.assertTrue(os.path.exists(f'{OUTPUT_PATH}/Box_Whisker_Plot_Pollutant_at_041_062_pm_25.png'))


    def test_by_multiple_variables_one_site(self):
        updated_dataframe = TimeSplit(dataframe, column_containing_dates, 8).split_dataframe()
        melted_dataframe = MeltDataframe(updated_dataframe, 'pollutants', 'level_of_pollution',
                                         'day_of_week', ['pm_25', 'pm_10'], dataframe_containing_device_id=updated_dataframe).get_melted_dataframe()
        BoxWhiskerGraph(melted_dataframe, 'level_of_pollution', 'day_of_week', 'pollutants', output_directory=OUTPUT_PATH).box_whisker_graph()
        self.assertTrue(os.path.exists(f'{OUTPUT_PATH}/Box_Whisker_Plot_day_of_week_at_276_TARA041_range_pollutants.png'))

    def test_one_site_multiple_variables_overall(self):
        updated_dataframe = TimeSplit(dataframe, column_containing_dates, 1).split_dataframe()
        focused_dataframe = updated_dataframe[['pm_25', 'pm_10', 'no2']]
        df_melted = MeltDataframe(focused_dataframe, variables_name='Pollutant', values_name='value', dataframe_containing_device_id=updated_dataframe).get_melted_dataframe()
        BoxWhiskerGraph(df_melted, 'value', 'Pollutant',
                        output_directory=OUTPUT_PATH).box_whisker_graph()
        self.assertTrue(os.path.exists(f'{OUTPUT_PATH}/Box_Whisker_Plot_Pollutant_at_276_TARA041.png'))

    def test_one_site_multiple_variables_overall_with_cleaned_data(self):
        cleaned_dataframe = CleanData(dataframe).remove_anomalies()
        updated_dataframe = TimeSplit(cleaned_dataframe, column_containing_dates, 1).split_dataframe()
        focused_dataframe = updated_dataframe[['pm_25', 'pm_10', 'no2']]
        df_melted = MeltDataframe(focused_dataframe, variables_name='Pollutant', values_name='value',
                                  dataframe_containing_device_id=updated_dataframe).get_melted_dataframe()
        BoxWhiskerGraph(df_melted, 'value', 'Pollutant',
                        output_directory=OUTPUT_PATH).box_whisker_graph()
        self.assertTrue(os.path.exists(f'{OUTPUT_PATH}/Box_Whisker_Plot_Pollutant_at_276_TARA041.png'))

if __name__ == '__main__':
    unittest.main()
