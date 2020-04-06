import os
import sys

from PyQt4 import QtGui

from src.covid19_nz_data_processing.app.ui_plot_app import Ui_MainWindow
from src.covid19_nz_data_processing.main import Basic


class PlotWidget(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(PlotWidget, self).__init__(parent)

        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        self._make_connections()
        self.showNormal()

    def _make_connections(self):
        self._ui.open.clicked.connect(self._plot)

    @staticmethod
    def _plot():
        import matplotlib.pyplot as plt

        run_data = Basic()
        run_data.plot_daily_trend()
        run_data.plot_cumulative_sum()

        plt.show()
