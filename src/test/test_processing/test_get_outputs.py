import unittest
import os
import pandas as pd

from processing.box_whisker_graphs import BoxWhiskerGraph, MeltDataframe
from processing.clean_data import CleanData
from processing.descriptive_stats import DescriptiveStats
from processing.dispersion_graphs import DispersionGraph
from processing.heatmap import Heatmap
from processing.line_graphs import LineGraphs
from processing.scatter_graphs import ScatterGraph
from processing.time_split import TimeSplit

CURRENT_PATH = os.getcwd()
four_levels_up = os.path.abspath(os.path.join(CURRENT_PATH, '..', '..', '..', '..'))


# Change
date_coverage_for_data_path = '020924_090924'
prefixes = ['004', '008', '011', '015', '024', '029', '036', '041', '044', '071']
number_of_groups_per_day = 8
DATA_PATH = f'{four_levels_up}/Data/Gurugram'
OUTPUT_PATH = f'{four_levels_up}/Coding/outputs/one_week_ten_sites_8_groups_Gurugram_ppt'
locations_text = '10_gurugram'

# prefixes = ['012', '017', '018', '030', '032', '047', '061', '062', '073', '086']
# number_of_groups_per_day = 8
# DATA_PATH = f'{four_levels_up}/Data/Patna'
# OUTPUT_PATH = f'{four_levels_up}/Coding/outputs/one_week_ten_sites_8_groups_Patna_ppt'
# locations_text = '10_patna'

dataframes = []

for prefix in prefixes:
    data_file = f'{DATA_PATH}/data_{prefix}_{date_coverage_for_data_path}.csv'
    dataframe = pd.read_csv(data_file)
    sorted_dataframe = dataframe.sort_values(by='data_created_time')
    dataframes.append(sorted_dataframe)

column_containing_dates = 'data_created_time'
variables_list = ['pm_25', 'pm_10', 'no2', 'co', 'temp', 'rh']

locations_with_pm_25 = [s + '_pm_25' for s in prefixes]
locations_with_pm_10 = [s + '_pm_10' for s in prefixes]
locations_with_no2 = [s + '_no2' for s in prefixes]
locations_with_co = [s + '_co' for s in prefixes]
locations_with_temp = [s + '_temp' for s in prefixes]
locations_with_rh = [s + '_rh' for s in prefixes]

locations_with_pollutant = [locations_with_pm_25, locations_with_pm_10, locations_with_no2, locations_with_co, locations_with_temp, locations_with_rh]

time_groups = ['day_of_week', 'group_time', 'hour']
descriptive_stats_groups = ['mean', 'max', 'min', 'range', 'iqr', 'std'] # need to add median

output_path = f'{OUTPUT_PATH}/test_outputs'


class MyTestCase(unittest.TestCase):
    def test_r2_all(self):
        clean_dataframes = []

        for dataframe in dataframes:
            clean_dataframe = CleanData(dataframe=dataframe).remove_anomalies()
            clean_dataframes.append(clean_dataframe)
        combined_dataframe = pd.concat(clean_dataframes, ignore_index=True)
        ScatterGraph(combined_dataframe, ['pm_25', 'pm_10', 'temp', 'rh'], output_directory=OUTPUT_PATH, combined=True).scatter_graph()
        self.assertEqual(True, True)

    def test_outputs_into_directory(self):
        time_split_multiple = []
        clean_dataframes = []
        overall_descriptive_stats = []
        for dataframe in dataframes:
            clean_dataframe = CleanData(dataframe=dataframe).remove_anomalies()
            clean_dataframes.append(clean_dataframe)
            overall_descriptive_stats.append(
                DescriptiveStats([clean_dataframe], variables_list, output_directory=OUTPUT_PATH).get_stats())

            time_split_multiple.append(TimeSplit(clean_dataframe, column_containing_dates, number_of_groups_per_day).split_dataframe())
        descriptive_stats_dataframe_group_time = DescriptiveStats(time_split_multiple, variables_list, time_group='group_time',
                                                                     output_directory=OUTPUT_PATH).get_stats()
        descriptive_stats_dataframe_hour = DescriptiveStats(time_split_multiple, variables_list,
                                                                  output_directory=OUTPUT_PATH,
                                                                  time_group='hour').get_stats()
        descriptive_stats_dataframe_date = DescriptiveStats(time_split_multiple, variables_list,
                                                                  output_directory=OUTPUT_PATH,
                                                                  time_group='date').get_stats()


        prefixed_dataframes = []
        for clean_dataframe, prefix in zip(clean_dataframes, prefixes):
            dataframe_prefixed = clean_dataframe.add_prefix(f'{prefix}_')
            prefixed_dataframes.append(dataframe_prefixed.rename(columns={f'{prefix}_data_created_time': 'data_created_time'}))
            # ScatterGraph(clean_dataframe, variables_list,
            #              output_directory=OUTPUT_PATH).scatter_graph()

        # Merging DataFrames on 'data_created_time' column - need to do with the one that started earlier first

        # Initialize the merged DataFrame
        merged_dataframe = prefixed_dataframes[0]
        # Iterate and merge
        for dataframe in prefixed_dataframes[1:]:
            merged_dataframe = merged_dataframe.merge(dataframe, on='data_created_time', how='outer')

        # merged_dataframe_sorted = merged_dataframe.sort_values(by='data_created_time')

        # updated_merged_dataframe = TimeSplit(merged_dataframe_sorted, column_containing_dates, number_of_groups_per_day).split_dataframe()

        # for location_with_pollutant, prefix in zip(locations_with_pollutant, prefixes):
        #     LineGraphs(merged_dataframe_sorted, location_with_pollutant, 'data_created_time', locations=f'{locations_text}_{prefix}',
        #            output_directory=OUTPUT_PATH).line_plot()
        #     focused_dataframe = updated_merged_dataframe[location_with_pollutant]
        #     value = location_with_pollutant[0][4:]
        #     df_melted = focused_dataframe.melt(var_name='Device', value_name=value)
        #     df_melted['Device'] = df_melted['Device'].str.replace(f'_{value}', '')
        #     BoxWhiskerGraph(df_melted, value, 'Device', locations=f'{locations_text}_{value}',
        #                     output_directory=OUTPUT_PATH).box_whisker_graph()
        #
        #     for x_column in time_groups:
        #         DispersionGraph(updated_merged_dataframe,
        #                         location_with_pollutant, x_column,
        #                         locations_stat_variable=locations_text, output_directory=OUTPUT_PATH).dispersion_graph()
        #         melted_dataframe = MeltDataframe(updated_merged_dataframe, 'locations', value, x_column,
        #                                          location_with_pollutant,
        #                                          location_more_than_one=True).get_melted_dataframe()
        #         melted_dataframe['locations'] = melted_dataframe['locations'].str.replace(f'_{value}', '')
        #
        #         BoxWhiskerGraph(melted_dataframe, value, x_column, multiple='locations',
        #                         locations=locations_text,
        #                         output_directory=OUTPUT_PATH).box_whisker_graph()


        for dataframe in clean_dataframes:
            # LineGraphs(dataframe, ['pm_25', 'pm_10', 'no2'], 'data_created_time', output_directory=OUTPUT_PATH).line_plot()
            for variable in variables_list:
                for group in time_groups:
                    BoxWhiskerGraph(dataframe, variable, group, output_directory=OUTPUT_PATH).box_whisker_graph()

        for variable in variables_list:
            focused_descriptive_stats_dataframe_group = descriptive_stats_dataframe_group_time[descriptive_stats_dataframe_group_time['variable'] == variable]
            focused_descriptive_stats_dataframe_hour = descriptive_stats_dataframe_hour[descriptive_stats_dataframe_hour['variable'] == variable]
            focused_descriptive_stats_dataframe_date = descriptive_stats_dataframe_date[descriptive_stats_dataframe_date['variable'] == variable]

            for dataframe, group in zip([focused_descriptive_stats_dataframe_group, focused_descriptive_stats_dataframe_hour,
                              focused_descriptive_stats_dataframe_date], ['group_time', 'hour', 'date']):
                for descriptive_stat in descriptive_stats_groups:
                    DispersionGraph(dataframe, [descriptive_stat], group, locations_stat_variable=f'{locations_text}_{descriptive_stat}_{variable}',
                                    output_directory=OUTPUT_PATH).dispersion_graph()
                    Heatmap(dataframe, descriptive_stat, group, 'device_id', locations=f'{locations_text}_{descriptive_stat}_{variable}', output_directory=OUTPUT_PATH).heatmap_plot()


        self.assertEqual(True, True)


    def test_outputs_focused(self):
        time_split_multiple = []
        clean_dataframes = []
        overall_descriptive_stats = []
        for dataframe in dataframes:
            clean_dataframe = CleanData(dataframe=dataframe).remove_anomalies()
            clean_dataframes.append(clean_dataframe)
            overall_descriptive_stats.append(
                DescriptiveStats([clean_dataframe], variables_list, output_directory=output_path).get_stats())

            time_split_multiple.append(TimeSplit(clean_dataframe, column_containing_dates, number_of_groups_per_day).split_dataframe())


        prefixed_dataframes = []
        for clean_dataframe, prefix in zip(clean_dataframes, prefixes):
            dataframe_prefixed = clean_dataframe.add_prefix(f'{prefix}_')
            prefixed_dataframes.append(dataframe_prefixed.rename(columns={f'{prefix}_data_created_time': 'data_created_time'}))

        # Merging DataFrames on 'data_created_time' column - need to do with the one that started earlier first

        # Initialize the merged DataFrame
        merged_dataframe = prefixed_dataframes[0]
        # Iterate and merge
        for dataframe in prefixed_dataframes[1:]:
            merged_dataframe = merged_dataframe.merge(dataframe, on='data_created_time', how='outer')

        merged_dataframe_sorted = merged_dataframe.sort_values(by='data_created_time')

        updated_merged_dataframe = TimeSplit(merged_dataframe_sorted, column_containing_dates,
                                             number_of_groups_per_day).split_dataframe()

        for location_with_pollutant, prefix in zip(locations_with_pollutant, prefixes):
            for x_column in time_groups:
                DispersionGraph(updated_merged_dataframe,
                                location_with_pollutant, x_column,
                                locations_stat_variable=locations_text, output_directory=output_path).dispersion_graph()

        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()
