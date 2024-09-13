import os
import unittest
from sqlite3 import Timestamp

import pandas as pd

from processing.clean_data import CleanData

CURRENT_PATH = os.getcwd()
four_levels_up = os.path.abspath(os.path.join(CURRENT_PATH, '..', '..', '..', '..'))
DATA_PATH = f'{four_levels_up}/Data'
data_file = f'{DATA_PATH}/data_041_280824_020924.csv'
dataframe = pd.read_csv(data_file)


class MyTestCase(unittest.TestCase):
    def test_remove_anomalies(self):
        cleaned_dataframe = CleanData(dataframe).remove_anomalies()
        self.assertLess(len(cleaned_dataframe), len(dataframe))  # add assertion here

    def test_where_one_missing_data(self):
        cleaned_dataframe = CleanData(dataframe).remove_anomalies()
        missing_data = CleanData(cleaned_dataframe).find_missing_intervals('data_created_time', 60)
        print(missing_data)
        self.assertEqual(missing_data, ["('2024-09-01 22:30:00+0000 - 2024-09-02 10:24:00+0000')"])

    def test_where_multiple_missing_data(self):
        cleaned_dataframe = CleanData(dataframe).remove_anomalies()
        missing_data = CleanData(cleaned_dataframe).find_missing_intervals('data_created_time', 2)
        print(missing_data)
        self.assertEqual(missing_data, ["('2024-08-29 22:52:00+0000 - 2024-08-29 22:53:00+0000')",
                                        "('2024-08-30 13:29:00+0000 - 2024-08-30 13:30:00+0000')",
                                        "('2024-08-30 16:14:00+0000 - 2024-08-30 16:15:00+0000')",
                                        "('2024-08-31 12:13:00+0000 - 2024-08-31 12:14:00+0000')",
                                        "('2024-09-01 21:32:00+0000 - 2024-09-02 10:24:00+0000')"])


if __name__ == '__main__':
    unittest.main()
