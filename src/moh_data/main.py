from src.moh_data.core.collector import DataCollector
from src.moh_data.utils.visualisation import Visualisation


class Basic:

    def __init__(self):
        self._excel_file = DataCollector()
        self._confirmed = None
        self._probable = None
        self._total_daily_confirmed = None
        self._total_daily_probable = None
        self._total_combined = None
        self._grand_sum = None

        self._vis = Visualisation()

        self._run()

    def _run(self):
        self._confirmed = self._excel_file.parse_confirmed()
        self._probable = self._excel_file.parse_probable()
        self._total_daily_confirmed = self._excel_file.get_daily_sum_confirmed()
        self._total_daily_probable = self._excel_file.get_daily_sum_probable()
        self._total_combined = self._excel_file.get_cumulative_sum()
        self._grand_sum = self._excel_file.get_grand_sum()
        self._total_arrival = self._excel_file.get_cumulative_arrival_sum()

    def plot_daily_trend(self):
        self._vis.set_data(self._total_combined, tick_interval=(2.0, 5.0))

    def plot_cumulative_sum(self):
        self._vis.set_data(self._grand_sum, tick_interval=(2.0, 100.0))

    def plot_cumulative_arrival_sum(self):
        self._vis.set_data(self._total_arrival, tick_interval=(2.0, 5.0))


if __name__ == '__main__':
    run_data = Basic()
    run_data.plot_daily_trend()
    run_data.plot_cumulative_sum()
    run_data.plot_cumulative_arrival_sum()
