from matplotlib import pyplot as plt
import seaborn as sns

from processing.Formatting import format_string, get_units, get_pollutant_name

class BoxWhiskerGraph:
    def __init__(self, dataframe, variable, x_column, multiple=None, locations=None, output_directory=None):
        self.dataframe = dataframe.sort_values(x_column)
        self.variable = variable
        if locations is None:
            self.device_id = dataframe['device_id'].iloc[0]
        else:
            self.device_id = None
        self.x_column = x_column
        self.location = locations
        self.multiple = multiple  # locations only needs to be completed if there is more than one location
        self.output_directory = output_directory  # only needs to be completed if the graph is to be saved
        self.units = get_units(variable)
        self.pollutant_name = get_pollutant_name(variable)
        # multiple could be multiple locations or variables. See MeltDataframe class - will the the same as 'variables_name'
        # location only needs to be added if more than one location is included

    def box_whisker_graph(self):
        if self.output_directory is None:
            self._get_box_whisker_plot()
            plt.show()
        else:
            self._get_box_whisker_plot()
            if self.location is None:
                if self.multiple is None:
                    plt.savefig(f'{self.output_directory}/Box_Whisker_Plot_{self.x_column}_{self.variable}_at_{self.device_id.replace(" | ", "_")}.png')
                else:
                    plt.savefig(f'{self.output_directory}/Box_Whisker_Plot_{self.x_column}_{self.variable}_at_{self.device_id.replace(" | ", "_")}_range_pollutants.png')
            else:
                plt.savefig(f'{self.output_directory}/Box_Whisker_Plot_{self.x_column}_{self.variable}_at_{self.location}.png')

            plt.close()

    def _get_box_whisker_plot(self):
        sns.set_theme(style="ticks", palette="pastel")
        if self.multiple is None:
            dataframe_cleaned = self.dataframe.dropna(subset=[self.x_column, self.variable])
            sns.boxplot(x=self.x_column, y=self.variable, data=dataframe_cleaned)
        else:
            sns.boxplot(x=self.x_column, y=self.variable, hue=self.multiple, data=self.dataframe)

        plt.suptitle('')  # Suppress the default title to avoid duplication
        if self.x_column == 'day_of_week':
            x_column_name = 'Week Day'
        elif self.x_column == 'group_time':
            x_column_name = 'Time'
        else:
            x_column_name = self.x_column

        plt.xlabel(format_string(x_column_name))
        plt.ylabel(f'{self.pollutant_name} {self.units}')
        plt.xticks(rotation=45)
        if self.multiple is not None:
            plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.tight_layout()

class MeltDataframe:
    def __init__(self, dataframe, variables_name, values_name, column_for_x_axis=None, list_of_columns_for_multiple_variables=None, location_more_than_one=False, dataframe_containing_device_id=None):
        self.dataframe = dataframe
        self.column_for_x_axis = column_for_x_axis
        self.list_of_columns_for_multiple_variables = list_of_columns_for_multiple_variables
        self.variables_name = variables_name
        self.values_name = values_name
        self.location_more_than_one = location_more_than_one
        self.dataframe_containing_device_id = dataframe_containing_device_id

    def get_melted_dataframe(self):
        if self.column_for_x_axis is not None:
            melted_dataframe =  self.dataframe.melt(id_vars=self.column_for_x_axis,
                                   value_vars=self.list_of_columns_for_multiple_variables,
                                   value_name=self.values_name,
                                   var_name=self.variables_name)
        else:
            melted_dataframe = self.dataframe.melt(value_name=self.values_name,
                                                   var_name=self.variables_name)
        if not self.location_more_than_one:
            device_id = self.dataframe_containing_device_id['device_id'].iloc[0]
            melted_dataframe['device_id'] = device_id
        return melted_dataframe

