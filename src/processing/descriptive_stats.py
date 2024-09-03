import pandas as pd

class DescriptiveStats:
    def __init__(self, dataframe, list_of_variables, output_directory=None):
        self.dataframe = dataframe
        self.list_of_variables = list_of_variables
        self.device_id = dataframe['device_id'].iloc[0]
        self.output_directory = output_directory

    def get_stats(self):
        output_dictionary = {}
        for variable in self.list_of_variables:
            variable_mean = self.get_mean(variable)
            variable_max = self.get_max(variable)
            variable_min = self.get_min(variable)
            variable_range = variable_max - variable_min
            variable_std = self.get_std(variable)
            variable_iqr = self.get_iqr(variable)
            output_dictionary[variable] = {'device_id': self.device_id, 'mean': variable_mean, 'max': variable_max, 'min': variable_min,
                                   'range': variable_range, 'std': variable_std, 'iqr': variable_iqr}
        output_dataframe = pd.DataFrame.from_dict(output_dictionary, orient='index')
        output_dataframe.reset_index(inplace=True)
        output_dataframe.rename(columns={'index': 'variable'}, inplace=True)

        if self.output_directory is not None:
            updated_device_id = self.device_id.replace(" | ", "_")
            output_name = f'descriptive_stats_{updated_device_id}.csv'
            output_path = f'{self.output_directory}/{output_name}'
            output_dataframe.to_csv(output_path, index=False)

        return output_dataframe


    def get_mean(self, variable):
        return self.dataframe[variable].mean()

    def get_max(self, variable):
        return self.dataframe[variable].max()

    def get_min(self, variable):
        return self.dataframe[variable].min()

    def get_std(self, variable):
        return self.dataframe[variable].std()

    def get_iqr(self, variable):
        return self.dataframe[variable].quantile(0.75) - self.dataframe[variable].quantile(0.25)



