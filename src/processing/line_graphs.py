import pandas as pd
from matplotlib import pyplot as plt

from processing.Formatting import get_units, get_pollutant_name, get_who_air_quality_guideline


class LineGraphs:
    def __init__(self, dataframe: pd.DataFrame, variables: list, x_column: str, locations=None, output_directory=None):
        self.dataframe = dataframe.sort_values(x_column)
        self.variables = variables
        if locations is None:
            self.device_id = dataframe['device_id'].iloc[0]
        else:
            self.device_id = None
        self.x_column = x_column
        self.locations = locations  # locations only needs to be completed if there is more than one location
        self.output_directory = output_directory  # only needs to be completed if the graph is to be saved
        self.variable_string = '_'.join(variables)

    def line_plot(self):
        if self.output_directory is None:
            self.get_line_plot()
            plt.show()
        else:
            self.get_line_plot()
            if self.locations is None:
                plt.savefig(
                    f'{self.output_directory}/Line_Plot_{self.x_column}_{self.variable_string}_at_{self.device_id.replace(" | ", "_")}.png')
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
            plt.plot(self.dataframe[self.x_column], self.dataframe[column], label=variable_name)

            y_label_list.append(f'{variable_name},')
        variable_units = get_units(self.variables[0])
        y_label_list.append(f'({variable_units})')
        # Adding title and labels
        plt.title('Temporal Changes in Pollution')
        plt.xlabel('Time')
        plt.ylabel(' '.join(y_label_list))

        self._add_lines_pollutant_levels()

        # Adding legend
        if len(self.variables) > 1:
            plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        if pd.api.types.is_datetime64_any_dtype(self.dataframe[self.x_column]):
            self.dataframe[self.x_column] = self.dataframe[self.x_column].dt.strftime('%Y-%m-%d')
            plt.xticks(self.dataframe[self.x_column][::step], rotation=45)
        else:
            short_labels = [label[:10] for label in self.dataframe[self.x_column][::step]]
            plt.xticks(self.dataframe[self.x_column][::step], short_labels, rotation=45)
        plt.tight_layout()

    def _add_lines_pollutant_levels(self):
        limits_list = ['pm_25', 'pm_10', 'no2', 'co']
        colours = ['red', 'darkred', 'firebrick', 'lightcoral']
        for limit, colour in zip(limits_list, colours):
            if any(limit in s for s in self.variables):
                y_line = get_who_air_quality_guideline(limit)
                name = get_pollutant_name(limit)
                plt.axhline(y=y_line, color=colour, linestyle='--', label=f'{name} limit')
