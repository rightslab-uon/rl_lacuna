from processing.clean_data import CleanData
from processing.descriptive_stats import DescriptiveStats
from processing.time_split import TimeSplit


class Outputs:
    def __init__(self, dataframes, column_containing_dates, number_of_groups_per_day, variables_list, output_path):
        self.dataframes = dataframes
        self.column_containing_dates = column_containing_dates
        self.number_of_groups_per_day = number_of_groups_per_day
        self.variables_list = variables_list
        self.output_path = output_path

    def get_outputs(self):
        time_split_dataframes = []
        overall_descriptive_stats = []

        for dataframe in self.dataframes:
            clean_dataframe = CleanData(dataframe=dataframe).remove_anomalies()
            time_split_dataframes.append(TimeSplit(clean_dataframe, self.column_containing_dates, self.number_of_groups_per_day).split_dataframe())
            overall_descriptive_stats.append(DescriptiveStats([clean_dataframe], self.variables_list, self.output_path).get_stats())
        dataframe_of_time_split_descriptive_stats = DescriptiveStats(time_split_dataframes, self.variables_list, output_directory=self.output_path, time_split=True).get_stats()
        return {'time_split_dataframes': time_split_dataframes,
                'overall_descriptive_stats': overall_descriptive_stats,
                'time_split_descriptive_stats': dataframe_of_time_split_descriptive_stats}

# not working in here, just do in test setting for the time being, then sort

