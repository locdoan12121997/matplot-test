import sys
import matplotlib

matplotlib.use("Qt5Agg")
from PyQt5 import QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from igraph import Graph
import matplotlib.pyplot as plt
import numpy as np


graph = Graph.Read_GraphML("./NREN.graphml")


class DataBar(FigureCanvas):
    node_list = []
    edge_list = []

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)

        self.axes = self.fig.add_subplot(111)

        # self.axes.set_axis_off()

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.show()

    def setData(self, data):
        self.data = data

    def plotDataCount(self):
        data = self.data

        value = list(set(data))
        height = [data.count(x) for x in set(data)]

        self.figure.clear()

        # create an axis
        ax = self.figure.add_subplot(111)

        ax.bar(value, height)
        for i in range(len(value)):  # your number of bars
            plt.text(x=i,  # takes your x values as horizontal positioning argument
                     y=height[i] + 1,  # takes your y values as vertical positioning argument
                     s=height[i],  # the labels you want to add to the data
                     size=9)

        ax.xticks(np.arange(len(value)), value, rotation=90)

    def clearFigure(self):
        self.axes.set_axis_off()
        del (self.node_list[:])
        self.updateFigure()

    def updateFigure(self):
        self.draw()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = DataBar(width=30, height=22)
    sys.exit(app.exec_())
