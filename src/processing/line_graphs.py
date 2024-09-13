import pandas as pd
from matplotlib import pyplot as plt

from processing.Formatting import get_units, get_pollutant_name


class LineGraphs:
    def __init__(self, dataframe, variables, x_column, locations=None, output_directory=None):
        self.dataframe = dataframe.sort_values(x_column)
        self.variables = variables
        if locations is None:
            self.device_id = dataframe['device_id'].iloc[0]
        else:
            self.device_id = None
        self.x_column = x_column
        self.locations = locations # locations only needs to be completed if there is more than one location
        self.output_directory = output_directory # only needs to be completed if the graph is to be saved
        self.variable_string = '_'.join(variables)

    def line_plot(self):
        if self.output_directory is None:
            self.get_line_plot()
            plt.show()
        else:
            self.get_line_plot()
            if self.locations is None:
                plt.savefig(f'{self.output_directory}/Line_Plot_{self.x_column}_{self.variable_string}_at_{self.device_id.replace(" | ", "_")}.png')
            else:
                plt.savefig(f'{self.output_directory}/Line_Plot_{self.x_column}_at_{self.locations}.png')

            plt.close()

    def get_line_plot(self):
        plt.figure(figsize=(10, 6))
        y_label_list = []
        unique_values = self.dataframe[self.x_column].nunique()
        step = max(1, unique_values // 15)

        for column in self.variables:
            variable_name = get_pollutant_name(column)
            plt.plot(self.dataframe[self.x_column], self.dataframe[column], label= variable_name)

            y_label_list.append(f'{variable_name},')
        variable_units = get_units(self.variables[0])
        y_label_list.append(f'({variable_units})')
        # Adding title and labels
        plt.title('Temporal Changes in Pollution')
        plt.xlabel('Time')
        plt.ylabel(' '.join(y_label_list))
        # Adding legend
        if len(self.variables) > 1:
            plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        if pd.api.types.is_datetime64_any_dtype(self.dataframe[self.x_column]):
            plt.xticks(self.dataframe[self.x_column], rotation=45)
        else:
            short_labels = [label[:10] for label in self.dataframe[self.x_column][::step]]
            plt.xticks(self.dataframe[self.x_column][::step], short_labels, rotation=45)
        plt.tight_layout()