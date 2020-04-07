import matplotlib.ticker as plticker


class Visualisation:

    def __init__(self, size=(10, 6), kind=None):
        self._df = None

        self._ax = None

        self._size = size
        self._kind = kind
        self._tick_int = None

    def set_data(self, data, tick_interval=None):
        if self._df is not None:
            self._df = None
        self._df = data

        if tick_interval:
            self._tick_int = tick_interval
        self._plot()

    def _plot(self):
        if self._ax is not None:
            self._ax = None

        self._ax = self._df.plot(figsize=self._size)
        self._ax.grid(axis='y', linewidth=0.2)
        self._ax.grid(axis='x', linewidth=0.2)

        if self._tick_int:
            x_loc = plticker.MultipleLocator(base=self._tick_int[0])
            self._ax.xaxis.set_major_locator(x_loc)
            y_loc = plticker.MultipleLocator(base=self._tick_int[1])
            self._ax.yaxis.set_major_locator(y_loc)
