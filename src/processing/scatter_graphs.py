import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

from processing.Formatting import get_units, get_pollutant_name


class ScatterGraph:
    def __init__(self, dataframe: pd.DataFrame, variables: list, output_directory=None, combined=False):
        self.dataframe = dataframe
        self.variables = variables
        if combined is False:
            self.device_id = dataframe['device_id'].iloc[0]
        else:
            self.device_id = 'multiple_locations'
        self.output_directory = output_directory

    def scatter_graph(self):
        r2_dict = {}
        x = self.variables[0]
        updated_variables = self.variables[1:]
        _id = 0
        for _ in range(len(self.variables)-1):
            for y in updated_variables:
                dataframe_cleaned = self.dataframe.dropna(subset=[x, y])
                if not dataframe_cleaned.empty:
                    x_r2 = dataframe_cleaned[[x]]
                    y_r2 = dataframe_cleaned[y]
                    r2 = self.get_r2(x_r2, y_r2)
                    r2_dict[_id] = {'x': x, 'y':y, 'r2':r2}
                    _id += 1
                    self.save_plot(dataframe_cleaned, x, y, r2)
            x = updated_variables.pop(0)

        output_dataframe = pd.DataFrame.from_dict(r2_dict, orient='index')
        output_dataframe.reset_index(inplace=True)
        output_dataframe = output_dataframe.sort_values(by='r2', ascending=False)
        self.save_dataframe(output_dataframe)
        return output_dataframe

    def save_dataframe(self, output_dataframe):
        if self.output_directory is not None:
            updated_device_id = self.device_id.replace(" | ", "_")
            output_name = f'r2_{updated_device_id}.csv'
            output_path = f'{self.output_directory}/{output_name}'
            output_dataframe.to_csv(output_path, index=False)

    def save_plot(self, dataframe_cleaned, x, y,r2):
        if self.output_directory is not None:
            plot_title = self.get_scatter(dataframe_cleaned, x, y, r2)
            output_name = f'{self.output_directory}/{plot_title.replace(" ", "_")}.png'
            plt.savefig(output_name)
            plt.close()
        else:
            self.get_scatter(dataframe_cleaned, x, y, r2)
            plt.show()


    @staticmethod
    def get_r2(x_r2, y_r2):
        model = LinearRegression()
        model.fit(x_r2, y_r2)
        # Predict the response variable
        y_pred = model.predict(x_r2)
        # Calculate R² value
        return r2_score(y_r2, y_pred)

    def get_scatter(self, dataframe_cleaned, x, y, r2):
        plt.scatter(dataframe_cleaned[x].values, dataframe_cleaned[y].values, color='royalblue', s=100, marker='.')
        x_max = 0.9*max(dataframe_cleaned[x].values)
        y_max = max(dataframe_cleaned[y].values)
        plt.text(x_max, y_max, f'R2: {round(r2,4)}', ha='left', va='top', fontsize=10, color='darkblue')

        x_variable_name = get_pollutant_name(x)
        x_variable_units = get_units(x)
        y_variable_name = get_pollutant_name(y)
        y_variable_units = get_units(y)

        plot_title = f'Scatter Plot for {x_variable_name} and {y_variable_name} at {self.device_id.replace(" | ", " ")}'
        plt.title(plot_title)
        plt.xlabel(f'{x_variable_name} ({x_variable_units})')
        plt.ylabel(f'{y_variable_name} ({y_variable_units})')
        plt.xticks(rotation=45)
        plt.tight_layout()
        m, b = np.polyfit(dataframe_cleaned[x].values, dataframe_cleaned[y].values, 1)
        # Add the line of best fit to the plot
        plt.plot(dataframe_cleaned[x].values, m * dataframe_cleaned[x].values + b, color='darkblue')
        return plot_title
