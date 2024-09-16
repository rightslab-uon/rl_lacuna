import pandas as pd

class DescriptiveStats:
    def __init__(self, dataframes: list, list_of_variables: list, time_group=None, output_directory=None):
        self.dataframes = dataframes
        self.list_of_variables = list_of_variables
        self.output_directory = output_directory
        self.time_group = time_group

    def get_stats(self):
        output_dictionary = {}
        timing = 'group'

        for dataframe in self.dataframes:
            if self.time_group is None:
                dataframe['group'] = 0
                groups = [0]

            else:
                groups = dataframe[self.time_group].unique().tolist()
                timing = self.time_group


            device_id = dataframe['device_id'].iloc[0]
            for variable in self.list_of_variables:
                variable_mean = self._get_stat(dataframe, timing, variable, 'mean')
                variable_max = self._get_stat(dataframe, timing, variable, 'max')
                variable_min = self._get_stat(dataframe, timing, variable, 'min')
                variable_range = self._get_range(variable_max, variable_min)
                variable_std = self._get_stat(dataframe, timing, variable, 'std')
                variable_iqr = self._get_stat(dataframe, timing, variable, 'iqr')
                for group in range(len(groups)):
                    group_time = self._get_group_time(dataframe, group, groups)
                    output_dictionary[f'{variable}_{group}_{device_id}'] = {'device_id': device_id, 'variable': variable,
                                                                            'group': group, f'{timing}': group_time, 'mean': variable_mean[group],
                                                                'max': variable_max[group], 'min': variable_min[group],
                                                                'range': variable_range[group], 'std': variable_std[group],
                                                                'iqr': variable_iqr[group]}

        output_dataframe = self._dictionary_to_dataframe(output_dictionary)

        if len(self.dataframes) == 1:
            device_id = self.dataframes[0]['device_id'].iloc[0]
        else:
            device_id = 'multiple_locations'

        if self.output_directory is not None:
            self._save_csv(device_id, output_dataframe, timing)

        return output_dataframe

    def _get_group_time(self, dataframe, group, groups):
        if self.time_group in dataframe.columns:
            group_time = groups[group]
        else:
            group_time = '0:00-24:00'
        return group_time

    @staticmethod
    def _dictionary_to_dataframe(output_dictionary):
        output_dataframe = pd.DataFrame.from_dict(output_dictionary, orient='index')
        output_dataframe.reset_index(inplace=True)
        output_dataframe.rename(columns={'index': 'variable_group_device_id'}, inplace=True)
        return output_dataframe

    def _save_csv(self, device_id, output_dataframe, timing):
        updated_device_id = device_id.replace(" | ", "_")
        output_name = f'descriptive_stats_{updated_device_id}_groups_{timing}.csv'
        output_path = f'{self.output_directory}/{output_name}'
        output_dataframe.to_csv(output_path, index=False)

    def _get_stat(self, dataframe, group, variable, stat):
        if stat != 'iqr':
            dataframe_stat =  dataframe.groupby(group).agg({variable: stat}).reset_index()
        else:
            dataframe_stat = dataframe.groupby(group).agg({variable: self._iqr}).reset_index()
        return self._extract_relevant_outcomes_from_dataframe(dataframe_stat, variable)

    @staticmethod
    def _iqr(series):
        return series.quantile(0.75) - series.quantile(0.25)

    @staticmethod
    def _get_range(maximum, minimum):
        ranges = []
        for maximum, minimum in zip(maximum, minimum):
            ranges.append(maximum - minimum)
        return ranges

    @staticmethod
    def _extract_relevant_outcomes_from_dataframe(dataframe, variable):
        return dataframe[variable].to_list()

