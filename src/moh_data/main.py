import os

from .core.collector import DataCollector
from .utils.visualisation import Visualisation


class Basic:

    def __init__(self):
        self._excel_file = DataCollector()
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
        self._confirmed = self._excel_file.parse_confirmed()
        self._probable = self._excel_file.parse_probable()
        self._total_daily_confirmed = self._excel_file.get_daily_sum_confirmed()
        self._total_daily_probable = self._excel_file.get_daily_sum_probable()
        self._total_combined = self._excel_file.get_cumulative_sum()
        self._grand_sum = self._excel_file.get_grand_sum()
        self._total_arrival = self._excel_file.get_daily_arrival_sum()
        self._total_overseas_reported_date = self._excel_file.get_overseas_reported_sum()

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
