from matplotlib import pyplot as plt
import pandas as pd

from processing.Formatting import get_units, get_pollutant_name, get_who_air_quality_guideline


class DispersionGraph:
    def __init__(self, dataframe: pd.DataFrame, variables, x_column, locations_stat_variable=None, output_directory=None):
        self.dataframe = dataframe.sort_values(x_column)
        self.variables = variables
        if locations_stat_variable is None:
            self.device_id = dataframe['device_id'].iloc[0]
        else:
            self.device_id = None
        self.x_column = x_column
        self.locations = locations_stat_variable  # locations for name - only needs to be completed if there is more than one location
        self.output_directory = output_directory  # only needs to be completed if the graph is to be saved

    def dispersion_graph(self):
        if self.output_directory is None:
            self._get_dispersion_plot()
            plt.show()
        else:
            if self.locations is None:
                variable_name = self._get_dispersion_plot()
                plt.savefig(f'{self.output_directory}/Dispersion_Plot_{self.x_column}_{variable_name}_at_{self.device_id.replace(" | ", "_")}.png')
            else:
                variable_name = self._get_dispersion_plot()
                plt.savefig(f'{self.output_directory}/Dispersion_Plot_{self.x_column}_{variable_name}_at_{self.locations}.png')

            plt.close()

    def _get_dispersion_plot(self):
        if self.locations is None:
            for column in self.variables:
                variable_name = self._plot_multiple_variables_one_location(column)

        else:
            if len(self.variables) > 1:
                for column in self.variables:
                    variable_name = self._plot_multiple_variables_multiple_locations(column)

            else:
                variable = self.variables[0]
                pollutant = self.locations.split(f'{variable}_', 1)[1]
                variable_name = get_pollutant_name(pollutant)
                variable_units = get_units(pollutant)
                self._plot_multiple_locations_one_variable(variable, variable_name, variable_units)

        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.xlabel('Time')
        plt.xticks(rotation=45)
        plt.tight_layout()
        return variable_name

    def _plot_multiple_locations_one_variable(self, variable, variable_name, variable_units):
        _, ax = plt.subplots()
        for key, grp in self.dataframe.groupby(['device_id']):
            ax.scatter(grp[self.x_column], grp[variable] * len(grp), label=key)
        if variable_units == '':
            plt.ylabel(f'Pollutant {variable_name}')
        plt.ylabel(f'{variable} {variable_name} ({variable_units})')
        self._add_lines_pollutant_levels()

    def _plot_multiple_variables_multiple_locations(self, column):
        variable = self.variables[0]
        pollutant = variable[4:]
        variable_name = get_pollutant_name(pollutant)
        variable_units = get_units(pollutant)
        label = column[0:3]
        plt.scatter(self.dataframe[self.x_column].values, self.dataframe[column].values, s=10, marker='.',
                    label=label)
        if variable_units == '':
            plt.ylabel(f'Pollutant {variable_name}')
        plt.ylabel(f'{variable} {variable_name} ({variable_units})')
        self._add_lines_pollutant_levels()
        return variable_name

    def _plot_multiple_variables_one_location(self, column):
        plt.scatter(self.dataframe[self.x_column].values, self.dataframe[column].values, s=10, marker='.', label=column)
        variable_name = get_pollutant_name(column)
        variable_units = get_units(column)
        if variable_units == '':
            plt.ylabel(f'Pollutant {variable_name}')
        plt.ylabel(f'{variable_name} ({variable_units})')
        self._add_lines_pollutant_levels()
        return variable_name

    def _add_lines_pollutant_levels(self):
        limits_list = ['pm_25', 'pm_10', 'no2', 'co']
        colours = ['red', 'darkred', 'firebrick', 'lightcoral']
        for limit, colour in zip(limits_list, colours):
            if any(limit in s for s in self.variables):
                y_line = get_who_air_quality_guideline(limit)
                name = get_pollutant_name(limit)
                plt.axhline(y=y_line, color=colour, linestyle='--', label=f'{name} limit')




