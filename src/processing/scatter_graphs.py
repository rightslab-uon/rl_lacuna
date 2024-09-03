import pandas as pd
import matplotlib.pyplot as plt

class ScatterGraph:
    def __init__(self, dataframe, variables, output_path=None):
        self.dataframe = dataframe
        self.variables = variables
        self.device_id = dataframe['device_id'].iloc[0]
        self.output_path = output_path

    def scatter_graph(self):
        r2 =self.get_r2()
        x = self.variables[0]
        y = self.variables[1]
        plot_title = f'Scatter Plot for {x} and {y}'
        self.get_scatter()

    def get_r2(self):
        return self.dataframe[self.variables].corr()

    def get_scatter(self, x, y, plot_title):
        plt.scatter(self.dataframe[x], self.dataframe[y], color='red', s=100, marker='^')
        plt.title(plot_title)
        plt.xlabel(x)
        plt.ylabel(y)
        if self.output_path is not None:
            output_name = f'{self.output_path}_{plot_title}.png'
            plt.savefig(output_name)
        plt.show()