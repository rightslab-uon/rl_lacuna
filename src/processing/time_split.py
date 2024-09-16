import pandas as pd
import re

class DayNightSplit:
    def __init__(self, dataframe: pd.DataFrame, column_containing_dates: str, start_of_day: int, end_of_day: int):
        self.dataframe = dataframe
        self.column_containing_dates = column_containing_dates
        self.start_of_day = start_of_day
        self.end_of_day = end_of_day

    def split_dataframe(self):
        TimeSplit(self.dataframe, self.column_containing_dates).get_date_time_columns()
        TimeSplit(self.dataframe, self.column_containing_dates).get_hour_column()
        split_dictionary = self.groups()
        finder = GroupFinder()
        self.dataframe['group'] = self.dataframe['hour'].apply(lambda x: finder.find_group(split_dictionary, x))
        self.dataframe.replace({'group': {2: 'night'}}, inplace=True)
        return self.dataframe

    def groups(self):
        split_dictionary = {'night': {'start': 0, 'end': self.start_of_day},
                            'day': {'start': self.start_of_day, 'end': self.end_of_day},
                            2: {'start': self.end_of_day, 'end': 24}}
        return split_dictionary

class TimeSplit:
    def __init__(self, dataframe: pd.DataFrame, column_containing_dates: str, number_of_groups_per_day=24):
        self.dataframe = dataframe
        self.column_containing_dates = column_containing_dates
        self.number_of_splits_in_day = number_of_groups_per_day

    def split_dataframe(self):
        self.get_date_time_columns()
        self.get_hour_column()
        split_dictionary = self._get_groups()
        finder = GroupFinder()
        self.dataframe['group'] = self.dataframe['hour'].apply(lambda x: finder.find_group(split_dictionary, x))
        self.dataframe['group_time'] = self.dataframe['group'].apply(lambda x: f"{split_dictionary[x]['start']}-{split_dictionary[x]['end']}")
        self.dataframe['group_time'] = self.dataframe['group_time'].apply(self._add_colon_zeroes)
        updated_dataframe_tidy = self._get_tidier_group_time_column()
        return self._change_24_to_00(updated_dataframe_tidy)

    def _get_tidier_group_time_column(self):
        data = self.dataframe.copy()
        data.loc[:, 'group_time'] = data['group_time'].str.replace(r'(\b\d\b)', r'0\1', regex=True)
        return data

    @staticmethod
    def _change_24_to_00(dataframe):
        data = dataframe.copy()
        data.loc[data['group_time'].str.contains('24'), 'group_time'] = data['group_time'].str.replace('24', '00')
        return data

    def _get_groups(self):
        number_of_hours_per_split = int(24/self.number_of_splits_in_day)
        split_start = 0
        split_dictionary = {}
        number = 0
        for _ in range(self.number_of_splits_in_day):
            split_dictionary[number] = {'start': split_start, 'end': split_start + number_of_hours_per_split}
            number += 1
            split_start = split_start + number_of_hours_per_split
        return split_dictionary

    @staticmethod
    def _add_colon_zeroes(range_str):
        return re.sub(r'(\d+)', r'\1:00', range_str)

    def get_hour_column(self):
        self.dataframe['hour'] = self.dataframe[self.column_containing_dates].dt.hour

    def get_date_time_columns(self):
        self.dataframe[self.column_containing_dates] = pd.to_datetime(self.dataframe[self.column_containing_dates])
        self.dataframe['date'] = self.dataframe[self.column_containing_dates].dt.date
        self.dataframe['time'] = self.dataframe[self.column_containing_dates].dt.time
        self.dataframe['day_of_week'] = self.dataframe[self.column_containing_dates].dt.day_name()


class GroupFinder:
    @staticmethod
    def find_group(split_dictionary, hour):
        for key, range_dict in split_dictionary.items():
            if range_dict['start'] <= hour < range_dict['end']:
                return key