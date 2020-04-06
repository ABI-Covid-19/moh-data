import sys

from PyQt4 import QtGui

from src.moh_data.app.app_widget import PlotWidget


def main():
    app = QtGui.QApplication(sys.argv)
    app.setStyle(QtGui.QStyleFactory.create("Cleanlooks"))
    app.setPalette(QtGui.QApplication.style().standardPalette())
    ui = PlotWidget()
    sys.exit(app.exec_())


main()
