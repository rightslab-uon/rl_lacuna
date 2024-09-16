import numpy as np
import pandas as pd

pd.options.mode.chained_assignment = None


class CleanData:
    def __init__(self, dataframe: pd.DataFrame):
        self.dataframe = dataframe

    def remove_anomalies(self):
        for col in self.dataframe.select_dtypes(include=[np.number]).columns:
            lower_bound = self.dataframe[col].quantile(0.001)
            upper_bound = self.dataframe[col].quantile(0.999)
            return self.dataframe[(self.dataframe[col] >= lower_bound) & (self.dataframe[col] <= upper_bound)]

    def find_missing_intervals(self, column_containing_dates_times: str, minutes_missing: int):
        # Ensure the datetime column is in datetime format
        self.dataframe[column_containing_dates_times] = pd.to_datetime(self.dataframe[column_containing_dates_times])

        # Sort the dataframe by datetime
        self.dataframe = self.dataframe.sort_values(by=column_containing_dates_times)

        # Calculate the difference between consecutive rows
        self.dataframe['difference'] = self.dataframe[column_containing_dates_times].diff().dt.total_seconds() / 60.0

        # Find the intervals where the difference is greater than the specified minutes_missing
        missing_intervals = self.dataframe[self.dataframe['difference'] > minutes_missing]

        # Create a list of tuples with the start and end of the missing intervals
        # Create a list of tuples with the start and end of the missing intervals
        missing_times = [(row[column_containing_dates_times] - pd.Timedelta(minutes=row['difference']),
                          row[column_containing_dates_times]) for index, row in
                         missing_intervals.iterrows()]

        # Adjust the start time to reflect the actual end of the previous interval
        missing_times = [(start + pd.Timedelta(minutes=minutes_missing), end) for start, end in missing_times]

        updated_missing_times = []

        for missing_time in missing_times:
            start_time = missing_time[0].strftime('%Y-%m-%d %H:%M:%S%z')
            end_time = missing_time[1].strftime('%Y-%m-%d %H:%M:%S%z')
            formatted_string = f"('{start_time} - {end_time}')"
            updated_missing_times.append(formatted_string)

        return updated_missing_times
