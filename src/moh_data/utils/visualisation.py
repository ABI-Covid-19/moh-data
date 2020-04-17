import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

import pandas as pd


class Visualisation:

    def __init__(self, size=(10, 6), kind=None):
        self._df = None

        self._ax = None

        self._size = size
        self._kind = kind
        self._tick_int = None

    def set_data(self, data, tick_interval=None, save=None):
        if self._df is not None:
            self._df = None
        self._df = data

        if tick_interval:
            self._tick_int = tick_interval

        output_image = None
        if save:
            output_image = save

        self._plot(output_image)

    def _plot(self, output=None):
        if self._ax is not None:
            self._ax = None

        self._ax = self._df.plot(figsize=self._size)
        self._ax.grid(axis='y', linewidth=0.2)
        self._ax.grid(axis='x', linewidth=0.2)

        self._ax.set_xlim(pd.Timestamp(self._df.index.min()), pd.Timestamp(self._get_last_available_date()))

        if self._tick_int:
            x_loc = plticker.MultipleLocator(base=self._tick_int[0])
            self._ax.xaxis.set_major_locator(x_loc)
            y_loc = plticker.MultipleLocator(base=self._tick_int[1])
            self._ax.yaxis.set_major_locator(y_loc)

        if output:
            plt.savefig(output)

        plt.show()

    def _get_last_available_date(self):
        return self._df.index[self._df.index.argsort() == (len(self._df.index) - 2)][0]
