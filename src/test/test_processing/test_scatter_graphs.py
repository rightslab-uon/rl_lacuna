import unittest
import os
import pandas as pd

from preprocessing.clean_data import CleanData
from processing.scatter_graphs import ScatterGraph

CURRENT_PATH = os.getcwd()
four_levels_up = os.path.abspath(os.path.join(CURRENT_PATH, '..', '..', '..', '..'))
DATA_PATH = f'{four_levels_up}/Data'
data_file = f'{DATA_PATH}/data_041_280824_020924.csv'
data_file_second_location = f'{DATA_PATH}/data_062_260824_020924.csv'
dataframe = pd.read_csv(data_file)
dataframe_second_location = pd.read_csv(data_file_second_location)

OUTPUT_PATH = f'{four_levels_up}/Coding/outputs'


class MyTestCase(unittest.TestCase):
    def test_r2(self):
        r2_dataframe = ScatterGraph(dataframe, ['pm_25', 'pm_10']).scatter_graph()
        r2 = r2_dataframe['r2'].iloc[0]
        self.assertEqual(0.74, round(r2, 2))

    def test_saved_scatter_plot(self):
        ScatterGraph(dataframe, ['pm_25', 'pm_10'], output_directory=OUTPUT_PATH).scatter_graph()
        self.assertTrue(os.path.exists(f'{OUTPUT_PATH}/Scatter_Plot_for_pm_2.5_and_pm_10_at_276_TARA041.png'))

    def test_r2_with_multiple_variables(self):
        r2_dataframe = ScatterGraph(dataframe, ['pm_25', 'pm_10', 'co']).scatter_graph()
        r2 = r2_dataframe['r2'].iloc[1]
        self.assertEqual(0.02, round(r2, 2))

    def test_saved_scatter_plot_with_multiple_variables(self):
        ScatterGraph(dataframe, ['pm_25', 'pm_10', 'no2', 'co', 'temp', 'rh'],
                     output_directory=OUTPUT_PATH).scatter_graph()
        self.assertTrue(os.path.exists(f'{OUTPUT_PATH}/Scatter_Plot_for_co_and_rh_at_276_TARA041.png'))

    def test_output_dataframe_to_csv_in_output_directory(self):
        ScatterGraph(dataframe, ['pm_25', 'pm_10', 'no2', 'co', 'temp', 'rh'],
                     output_directory=OUTPUT_PATH).scatter_graph()
        self.assertTrue(os.path.exists(f'{OUTPUT_PATH}/r2_276_TARA041.csv'))

    def test_r2_with_concat_dataframe(self):
        dataframes = [dataframe, dataframe_second_location]
        clean_dataframes = []

        for frame in dataframes:
            clean_dataframe = CleanData(dataframe=frame).remove_anomalies()
            clean_dataframes.append(clean_dataframe)

        combined_dataframe = pd.concat(clean_dataframes, ignore_index=True)
        ScatterGraph(combined_dataframe, ['pm_25', 'pm_10'], output_directory=OUTPUT_PATH,
                     combined=True).scatter_graph()
        ScatterGraph(combined_dataframe, ['pm_25', 'pm_10'], output_directory=OUTPUT_PATH,
                     combined=True).scatter_graph()
        self.assertTrue(os.path.exists(f'{OUTPUT_PATH}/r2_multiple_locations.csv'))


if __name__ == '__main__':
    unittest.main()
