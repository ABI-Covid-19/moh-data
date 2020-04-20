from .query import FindExcelFile

import numpy as np
import pandas as pd


def _check_zero(data, cols):
    for col in cols:
        data[col] = data[col].replace({'0': np.nan, 0: np.nan})


def _filter_null(data):
    return data[data.index.notnull()]


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

        self._overseas_confirmed_total = None
        self._overseas_probable_total = None
        self._overseas_combined_sum = None

    def _initialize(self):
        fef = FindExcelFile()
        self._excel_file = fef.fetch_file()
        self._jhu = JohnsHopkins()

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

    def get_overseas_sum_confirmed(self):
        _check_zero(self._confirmed_sheet, ['Arrival date'])
        _was_overseas = self._confirmed_sheet.loc[self._confirmed_sheet['Overseas travel'] == 'Yes']
        self._overseas_confirmed_total = self._get_custom_sum(self._confirmed_sheet, 'Date of report',
                                                              'Overseas confirmed cases on the date of reported')

    def get_overseas_sum_probable(self):
        _check_zero(self._probable_sheet, ['Arrival date'])
        _was_overseas = self._probable_sheet.loc[self._probable_sheet['Overseas travel'] == 'Yes']
        self._overseas_probable_total = self._get_custom_sum(self._probable_sheet, 'Date of report',
                                                             'Overseas probable cases on the date of reported')

    def get_daily_arrival_sum(self):
        self._generate_arrival_date_combined_sum()
        self._arrival_combined_sum = _filter_null(self._arrival_combined_sum)
        return self._arrival_combined_sum

    def get_overseas_reported_sum(self):
        self._generate_overseas_reported_combined_sum()
        return self._overseas_combined_sum

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
        index = total.index
        names = index.names
        temp_index_list = list()
        for index in total.index:
            try:
                temp_index_list.append(pd.to_datetime(index, format="%Y-%m-%d %H:%M:%S"))
            except ValueError:
                temp_index_list.append(pd.to_datetime(index, format="%d/%m/%Y"))
        total.insert(0, names[0], temp_index_list)
        total = total.set_index(names[0])
        idx = pd.date_range(total.index.min(), total.index.max())
        total = total.reindex(idx, fill_value=0)
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

    def _generate_overseas_reported_combined_sum(self):
        if self._overseas_confirmed_total is None:
            self.get_overseas_sum_confirmed()
        if self._overseas_probable_total is None:
            self.get_overseas_sum_probable()

        self._overseas_combined_sum = pd.DataFrame()
        for df in [self._overseas_confirmed_total, self._overseas_probable_total]:
            self._overseas_combined_sum = self._overseas_combined_sum.combine_first(df)
        self._overseas_combined_sum = self._overseas_combined_sum.fillna(0)

        self._overseas_combined_sum['Total'] = self._overseas_combined_sum["Overseas confirmed cases on the date of " \
                                                                           "reported"] + \
                                               self._overseas_combined_sum["Overseas probable cases on the date of " \
                                                                           "reported"]

    def get_cumulative_recovered(self):
        return self._jhu.recovered

    def get_cumulative_dead(self):
        return self._jhu.dead


class JohnsHopkins(object):

    def __init__(self):
        # CONFIRMED_CASES = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data" \
        #                   "/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv "
        RECOVERED_CASES = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data" \
                          "/csse_covid_19_time_series/time_series_covid19_recovered_global.csv "
        DEATH_CASES = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data" \
                      "/csse_covid_19_time_series/time_series_covid19_deaths_global.csv "

        recovered = pd.read_csv(RECOVERED_CASES, index_col=None)
        dead = pd.read_csv(DEATH_CASES, index_col=None)

        self.recovered = recovered[recovered['Country/Region'] == 'New Zealand']
        self.recovered = self.recovered.drop(self.recovered.columns[[0, 1, 2, 3]], axis=1)
        self.dead = dead[dead['Country/Region'] == 'New Zealand']
        self.dead = self.dead.drop(self.dead.columns[[0, 1, 2, 3]], axis=1)
