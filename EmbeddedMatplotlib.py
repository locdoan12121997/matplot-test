import sys
import matplotlib

matplotlib.use("Qt5Agg")
from PyQt5 import QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from igraph import Graph

# Personal modules
from DraggablePoint import DraggablePoint
from DraggableLine import DraggableLine


graph = Graph.Read_GraphML("./NREN.graphml")


class MyGraph(FigureCanvas):
    node_list = []
    edge_list = []

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)

        self.axes = self.fig.add_subplot(111)
        # self.axes.set_xlim(-60.0, 60.0)
        # self.axes.set_ylim(-25.0, -75.0)
        # self.axes.set_axis_off()

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.show()

        # self.plotNodes(graph.vs)
        # self.plotLinks(graph.es)

    def plotDataCount(self, data):
        value = list(set(data))
        height = [data.count(x) for x in set(data)]


    def plotNodes(self, nodes, size=None):
        for node in nodes:
            node = DraggablePoint(self, node["x"], node["y"])
            self.node_list.append(node)
        self.updateFigure()

    def plotLinks(self, links):
        for link in links:
            node_a = self.node_list[link.source]
            node_b = self.node_list[link.target]

            edge = DraggableLine(self, link.index, node_a, node_b, color='g')

            node_a.lines.append(edge)
            node_b.lines.append(edge)
            self.edge_list.append(edge)
            self.fig.axes[0].add_line(edge)

    def clearFigure(self):
        self.axes.set_axis_off()
        del (self.node_list[:])
        self.updateFigure()

    def updateFigure(self):
        self.draw()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = MyGraph(width=30, height=22)
    sys.exit(app.exec_())
