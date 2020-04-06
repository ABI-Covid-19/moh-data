from .query import FindExcelFile

import pandas as pd


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

    def _initialize(self):
        fef = FindExcelFile()
        self._excel_file = fef.fetch_file()

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
    def _get_daily_sum(sheet, col):
        total_num = sheet['Date of report'].map(sheet.groupby('Date of report').size())
        total = pd.concat([sheet['Date of report'], total_num], axis=1).drop_duplicates()
        total.columns = ['Date of report', col]
        total.set_index('Date of report', inplace=True)
        total.index = pd.to_datetime(total.index)
        return total

    def get_daily_sum_confirmed(self):
        self._confirmed_total = self._get_daily_sum(self._confirmed_sheet, 'Daily total of confirmed')
        return self._confirmed_total

    def get_daily_sum_probable(self):
        self._probable_total = self._get_daily_sum(self._probable_sheet, 'Daily total of probable')
        return self._probable_total

    def generate_combined_sum(self):
        self._combined_sum = pd.DataFrame()
        for df in [self._confirmed_total, self._probable_total]:
            self._combined_sum = self._combined_sum.combine_first(df)
        self._combined_sum = self._combined_sum.fillna(0)

        self._combined_sum['Total'] = self._combined_sum["Daily total of confirmed"] + \
                                      self._combined_sum["Daily total of probable"]
        return self._combined_sum
