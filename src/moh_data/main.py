import os
from datetime import datetime

import numpy as np

try:
    from .core.collector import DataCollector
    from .utils.visualisation import Visualisation
except ImportError:
    from core.collector import DataCollector
    from utils.visualisation import Visualisation


class Basic:

    def __init__(self):
        self._database = DataCollector()
        self._confirmed = None
        self._probable = None
        self._total_daily_confirmed = None
        self._total_daily_probable = None
        self._total_combined = None
        self._grand_sum = None
        self._total_arrival = None
        self._total_overseas_reported_date = None

        self._vis = Visualisation()

        self._run()

    def _run(self):
        self._confirmed = self._database.parse_confirmed()
        self._probable = self._database.parse_probable()
        self._total_daily_confirmed = self._database.get_daily_sum_confirmed()
        self._total_daily_probable = self._database.get_daily_sum_probable()
        self._total_combined = self._database.get_cumulative_sum()
        self._grand_sum = self._database.get_grand_sum()
        self._total_arrival = self._database.get_daily_arrival_sum()
        self._total_overseas_reported_date = self._database.get_overseas_reported_sum()

    def get_cumulative_confirmed_cases_on_day(self, day):
        """
        Get the cumulative number of total confirmed cases on a particular date

        :param day: int corresponding to the day of which data is available for.
        :return:
        """
        return self._get_cases_on_day(self._grand_sum['Total confirmed cases'], day)

    def get_cumulative_probable_cases_on_day(self, day):
        """
        Get the cumulative number of total probable cases on a particular date

        :param day: int corresponding to the day of which data is available for.
        :return:
        """
        return self._get_cases_on_day(self._grand_sum['Total probable cases'], day)

    def get_cumulative_total_cases_on_day(self, day):
        """
        Get the cumulative number of total confirmed and probable cases on a particular date

        :param day: int corresponding to the day of which data is available for.
        :return:
        """
        return self._get_cases_on_day(self._grand_sum['Grand total'], day)

    @staticmethod
    def _get_cases_on_day(sheet, day):
        if isinstance(day, ("".__class__, u"".__class__)):
            day = int(day)
        elif isinstance(day, ([].__class__, ().__class__)):
            day = day[0]
        if day > len(sheet) - 1:
            raise ValueError("You entered {0}. Total number of days available are {1}."
                             .format(day, len(sheet) - 1))
        return int(sheet.iloc[day])

    def get_cumulative_recovered_cases_on(self, day):
        """
        Get the cumulative number of total recovered cases on a particular date

        :param day: int corresponding to the day of which data is available for.
        :return:
        """
        df = self._database.get_cumulative_recovered()
        return df[df.columns[day]].values[-1]

    def get_cumulative_dead_cases_on(self, day):
        """
        Get the cumulative number of total dead cases on a particular date

        :param day: int corresponding to the day of which data is available for.
        :return:
        """
        df = self._database.get_cumulative_dead()
        return df[df.columns[day]].values[-1]

    def get_confirmed_cases_on_date(self, date):
        """
        Get the number of confirmed cases on a particular date

        :param date: list with (month, day) format e.g. (04, 14).
        :return:
        """
        return self._get_cases_on_date(self._total_daily_confirmed, date)

    def get_confirmed_cases_between_dates(self, dates):
        """
        Get the number of confirmed cases between two dates

        :param dates: list of lists with ((month, day), (month, day)) format e.g. ((04, 08), (04, 14)).
        :return:
        """
        return self._get_cases_between_dates(self._total_daily_confirmed, dates)

    def get_probable_cases_on_date(self, date):
        """
        Get the number of probable cases on a particular date

        :param date: list with (month, day) format e.g. (04, 14).
        :return:
        """
        return self._get_cases_on_date(self._total_daily_probable, date)

    def get_probable_cases_between_dates(self, dates):
        """
        Get the number of probable cases between two dates

        :param dates: list of lists with ((month, day), (month, day)) format e.g. ((04, 08), (04, 14)).
        :return:
        """
        return self._get_cases_between_dates(self._total_daily_probable, dates)

    def get_cases_on_date(self, date):
        """
        Get the number of total confirmed and probable cases on a particular date

        :param date: list with (month, day) format e.g. (04, 14).
        :return:
        """
        return self._get_cases_on_date(self._total_combined.Total, date)

    def get_cases_between_dates(self, dates):
        """
        Get the number of total confirmed and probable cases between two dates

        :param dates: list of lists with ((month, day), (month, day)) format e.g. ((04, 08), (04, 14)).
        :return:
        """
        return self._get_cases_between_dates(self._total_combined.Total, dates)

    def get_cumulative_confirmed_cases_on_date(self, date):
        """
        Get the cumulative number of total confirmed cases on a particular date

        :param date: list with (month, day) format e.g. (04, 14).
        :return:
        """
        return self._get_cases_on_date(self._grand_sum['Total confirmed cases'], date)

    def get_cumulative_probable_cases_on_date(self, date):
        """
        Get the cumulative number of total probable cases on a particular date

        :param date: list with (month, day) format e.g. (04, 14).
        :return:
        """
        return self._get_cases_on_date(self._grand_sum['Total probable cases'], date)

    def get_cumulative_total_cases_on_date(self, date):
        """
        Get the cumulative number of total confirmed and probable cases on a particular date

        :param date: list with (month, day) format e.g. (04, 14).
        :return:
        """
        return self._get_cases_on_date(self._grand_sum['Grand total'], date)

    @staticmethod
    def _get_cases_on_date(sheet, date):
        if len(sheet[sheet.index == datetime(2020, date[0], date[1])]) > 0:
            return int(sheet[sheet.index == datetime(2020, date[0], date[1])].values.flatten()[0])
        else:
            return 0

    @staticmethod
    def _get_cases_between_dates(sheet, dates):
        date_one = datetime(2020, dates[0][0], dates[0][1])
        date_two = datetime(2020, dates[1][0], dates[1][1])

        lesser = date_one if date_one < date_two else date_two
        greater = date_two if lesser != date_two else date_one

        mask = (sheet.index > lesser) & (sheet.index <= greater)
        if isinstance(sheet.loc[mask].sum(), np.float):
            return int(sheet.loc[mask].sum())
        elif len(sheet.loc[mask]) > 0:
            return int(sheet.loc[mask].sum().values.flatten()[0])
        else:
            return 0

    def get_daily_data(self):
        return self._total_combined

    def get_daily_cumulative_data(self):
        return self._grand_sum

    def get_date_of_arrival_of_overseas_cases_data(self):
        return self._total_arrival

    def get_date_of_reported_of_overseas_cases_data(self):
        return self._total_overseas_reported_date

    def plot_daily_trend(self, s=None):
        self._vis.set_data(self._total_combined, tick_interval=(2.0, 5.0), save=s)

    def plot_cumulative_sum(self, s=None):
        self._vis.set_data(self._grand_sum, tick_interval=(2.0, 100.0), save=s)

    def plot_daily_arrival_sum(self, s=None):
        self._vis.set_data(self._total_arrival, tick_interval=(2.0, 5.0), save=s)

    def plot_overseas_date_reported(self, s=None):
        self._vis.set_data(self._total_overseas_reported_date, tick_interval=(2.0, 5.0), save=s)

    @staticmethod
    def export_data(data, filename):
        if 'csv' not in os.path.basename(filename):
            filename += '.csv'
        data.to_csv(filename, sep=',')
        return


if __name__ == '__main__':
    run_data = Basic()
    save = False
    if save:
        op = '../../resources/'
        run_data.plot_daily_trend(s='{}Figure_1'.format(op))
        run_data.plot_cumulative_sum(s='{}Figure_2'.format(op))
        run_data.plot_daily_arrival_sum(s='{}Figure_3'.format(op))
        run_data.plot_overseas_date_reported(s='{}Figure_4'.format(op))
    else:
        run_data.plot_daily_trend()
        run_data.plot_cumulative_sum()
        run_data.plot_daily_arrival_sum()
        run_data.plot_overseas_date_reported()

        print('Cumulative confirmed cases on day 40 = ', run_data.get_cumulative_confirmed_cases_on_day(40))
        print('Cumulative probable cases on day 40 = ', run_data.get_cumulative_probable_cases_on_day(40))
        print('Cumulative total cases on day 40 = ', run_data.get_cumulative_total_cases_on_day(40))
        print('Cumulative recovered cases on day 80 = ', run_data.get_cumulative_recovered_cases_on(80))
        print('Cumulative dead cases on day 80 = ', run_data.get_cumulative_dead_cases_on(80))

        print('Confirmed cases on 2020-04-14 = ', run_data.get_confirmed_cases_on_date((4, 14)))
        print('Confirmed cases between 2020-04-08 and 2020-04-14 =',
              run_data.get_confirmed_cases_between_dates(((4, 8), (4, 14))))

        print('Probable cases on 2020-04-14 = ', run_data.get_probable_cases_on_date((4, 14)))
        print('Probable cases between 2020-04-08 and 2020-04-14 =',
              run_data.get_probable_cases_between_dates(((4, 8), (4, 14))))

        print('Total cases on 2020-04-14 = ', run_data.get_cases_on_date((4, 14)))
        print('Total cases between 2020-04-08 and 2020-04-14 =', run_data.get_cases_between_dates(((4, 8), (4, 14))))

        print('Cumulative confirmed cases on 2020-04-14 = ', run_data.get_cumulative_confirmed_cases_on_date((4, 14)))
        print('Cumulative probable cases on 2020-04-14 = ', run_data.get_cumulative_probable_cases_on_date((4, 14)))
        print('Cumulative total cases on 2020-04-14 = ', run_data.get_cumulative_total_cases_on_date((4, 14)))
