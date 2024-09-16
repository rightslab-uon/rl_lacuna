import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

from processing.Formatting import get_units, get_pollutant_name


class Heatmap:
    def __init__(self, descriptive_dataframe: pd.DataFrame, stats_variable: str, x_column: str, y_column: str, locations: str, output_directory=None):
        self.dataframe = descriptive_dataframe.sort_values(y_column)
        self.variable = stats_variable
        self.x_column = x_column
        self.y_column = y_column
        self.locations = locations
        self.unit = get_units(self.variable)
        self.variable_name = get_pollutant_name(self.variable)
        self.output_directory = output_directory  # only needs to be completed if the graph is to be saved
        # multiple could be multiple locations or variables. See MeltDataframe class - will the be same as 'variables_name'
        # location only needs to be added if more than one location is included


    def heatmap_plot(self):
        plt.close('all')
        if self.output_directory is None:
            self.get_heatmap()
            plt.show()
        else:
            self.get_heatmap()
            plt.savefig(f'{self.output_directory}/Heatmap_{self.x_column}_{self.variable}_at_{self.locations}.png')
            plt.close()

    def get_heatmap(self):
        plt.figure(figsize=(12, 8))
        category_order = list(self.dataframe[self.y_column].unique())
        category_order.sort()
        self.dataframe[self.y_column] = pd.Categorical(self.dataframe[self.y_column], categories=category_order, ordered = True)
        heatmap_data = self.dataframe.pivot(index=self.x_column, columns=self.y_column, values=self.variable)
        sns.heatmap(heatmap_data, cmap='coolwarm', annot=True)
        plt.xlabel('Place')
        plt.ylabel('Time')
        plt.xticks(rotation=45)
        plt.tight_layout()

