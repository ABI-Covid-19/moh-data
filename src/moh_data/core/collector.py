from .query import FindExcelFile

import numpy as np
import pandas as pd


def _check_zero(data, cols):
    for col in cols:
        data[col] = data[col].replace({'0': np.nan, 0: np.nan})


class DataCollector(object):

    def __init__(self, *args):
        self._excel_file = None

        if args:
            self._excel_file = args[0]
        else:
            self._initialize()

        self._confirmed_sheet = None
        self._probable_sheet = None

        self._confirmed_total = None
        self._probable_total = None
        self._combined_sum = None
        self._grand_sum = None

        self._arrival_confirmed_total = None
        self._arrival_probable_total = None
        self._arrival_combined_sum = None

    def get_daily_sum_confirmed(self):
        self._confirmed_total = self._get_custom_sum(self._confirmed_sheet, 'Date of report', 'Daily confirmed cases')
        return self._confirmed_total

    def get_daily_sum_probable(self):
        self._probable_total = self._get_custom_sum(self._probable_sheet, 'Date of report', 'Daily probable cases')
        return self._probable_total

    def get_cumulative_sum(self):
        self._generate_combined_sum()
        return self._combined_sum

    def get_grand_sum(self):
        self._grand_sum = self.get_cumulative_sum().cumsum()
        self._grand_sum.columns = ['Total confirmed cases', 'Total probable cases', 'Grand total']
        return self._grand_sum

    def get_arrival_sum_confirmed(self):
        _check_zero(self._confirmed_sheet, ['Arrival date'])
        self._arrival_confirmed_total = self._get_custom_sum(self._confirmed_sheet, 'Arrival date',
                                                             'Arrival date of daily confirmed cases')

    def get_arrival_sum_probable(self):
        _check_zero(self._probable_sheet, ['Arrival date'])
        self._arrival_probable_total = self._get_custom_sum(self._probable_sheet, 'Arrival date',
                                                            'Arrival date of daily probable cases')

    def get_daily_arrival_sum(self):
        self._generate_arrival_date_combined_sum()
        return self._arrival_combined_sum

    def _initialize(self):
        fef = FindExcelFile()
        self._excel_file = fef.fetch()

    def parse_confirmed(self):
        self._confirmed_sheet = pd.read_excel(self._excel_file,
                                              sheet_name='Confirmed',
                                              header=1,
                                              skiprows=range(1, 3))
        self._confirmed_sheet = self._confirmed_sheet.fillna(0)
        return self._confirmed_sheet

    def parse_probable(self):
        self._probable_sheet = pd.read_excel(self._excel_file,
                                             sheet_name='Probable',
                                             header=1,
                                             skiprows=range(1, 3))
        self._probable_sheet = self._probable_sheet.fillna(0)
        return self._probable_sheet

    @staticmethod
    def _get_custom_sum(sheet, current_col=None, desired_col=None):
        total_num = sheet[current_col].map(sheet.groupby(current_col).size())
        total = pd.concat([sheet[current_col], total_num], axis=1).drop_duplicates()
        total.columns = [current_col, desired_col]
        total.set_index(current_col, inplace=True)
        total.index = pd.to_datetime(total.index)
        return total

    def _generate_combined_sum(self):
        self._combined_sum = pd.DataFrame()
        for df in [self._confirmed_total, self._probable_total]:
            self._combined_sum = self._combined_sum.combine_first(df)
        self._combined_sum = self._combined_sum.fillna(0)

        self._combined_sum['Total'] = self._combined_sum["Daily confirmed cases"] + \
                                      self._combined_sum["Daily probable cases"]

    def _generate_arrival_date_combined_sum(self):
        if self._arrival_confirmed_total is None:
            self.get_arrival_sum_confirmed()
        if self._arrival_probable_total is None:
            self.get_arrival_sum_probable()

        self._arrival_combined_sum = pd.DataFrame()
        for df in [self._arrival_confirmed_total, self._arrival_probable_total]:
            self._arrival_combined_sum = self._arrival_combined_sum.combine_first(df)
        self._arrival_combined_sum = self._arrival_combined_sum.fillna(0)

        self._arrival_combined_sum['Total'] = self._arrival_combined_sum["Arrival date of daily confirmed cases"] + \
                                              self._arrival_combined_sum["Arrival date of daily probable cases"]

