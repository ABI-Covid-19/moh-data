from src.covid19_nz_data_processing.core.collector import DataCollector


class Basic:

    def __init__(self):
        self._excel_file = DataCollector()
        self._confirmed = None
        self._probable = None
        self._total_daily_confirmed = None
        self._total_daily_probable = None
        self._total_combined = None

        self._run()

    def _run(self):
        self._confirmed = self._excel_file.parse_confirmed()
        self._probable = self._excel_file.parse_probable()
        self._total_daily_confirmed = self._excel_file.get_daily_sum_confirmed()
        self._total_daily_probable = self._excel_file.get_daily_sum_probable()
        self._total_combined = self._excel_file.generate_combined_sum()

    def plot_daily_trend(self):
        self._total_combined.plot()

    def plot_cumulative_sum(self):
        self._total_combined.cumsum().plot()


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    run_data = Basic()
    run_data.plot_daily_trend()
    run_data.plot_cumulative_sum()

    plt.show()
