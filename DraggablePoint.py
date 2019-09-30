import matplotlib.patches as patches
from matplotlib.lines import Line2D


class DraggablePoint:
    lock = None
    id = None
    lines = []

    def __init__(self, parent, x, y, size=0.3):
        self.parent = parent
        self.point = patches.Circle((x, y), size, fill=True, fc='k', ec='g')

        self.x = x
        self.y = y

        parent.fig.axes[0].add_patch(self.point)
        self.press = None
        self.background = None

        self.connect()

    def connect(self):
        self.cidpress = self.point.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.point.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.point.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):

        if event.inaxes != self.point.axes:
            return
        if DraggablePoint.lock is not None:
            return
        contains, attrd = self.point.contains(event)
        if not contains:
            return
        self.press = self.point.center, event.xdata, event.ydata
        DraggablePoint.lock = self

        canvas = self.point.figure.canvas
        axes = self.point.axes

        self.point.set_animated(True)
        if len(self.lines) > 0:
            [line.set_animated(True) for line in self.lines]

        canvas.draw()
        self.background = canvas.copy_from_bbox(self.point.axes.bbox)

        axes.draw_artist(self.point)

        canvas.blit(axes.bbox)

    def on_motion(self, event):

        if DraggablePoint.lock is not self:
            return
        if event.inaxes != self.point.axes:
            return
        self.point.center, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        self.point.center = (self.point.center[0] + dx, self.point.center[1] + dy)

        canvas = self.point.figure.canvas
        axes = self.point.axes

        canvas.restore_region(self.background)

        axes.draw_artist(self.point)
        if len(self.lines) > 0:
            [axes.draw_artist(line) for line in self.lines]

        self.x = self.point.center[0]
        self.y = self.point.center[1]

        if len(self.lines) > 0:
            for line in self.lines:
                if self == line.end_a:
                    line_x = [line.end_b.x, self.x]
                    line_y = [line.end_b.y, self.y]
                    line.set_data(line_x, line_y)
                elif self == line.end_b:
                    line_x = [self.x, line.end_a.x]
                    line_y = [self.y, line.end_a.y]

                    for ln in line.end_a.lines:
                        if ln == line:
                            ln.set_data(line_x, line_y)

        canvas.blit(axes.bbox)

    def on_release(self, event):
        if DraggablePoint.lock is not self:
            return

        self.press = None
        DraggablePoint.lock = None

        self.point.set_animated(False)
        if len(self.lines) > 0:
            [line.set_animated(False) for line in self.lines]

        self.background = None

        self.point.figure.canvas.draw()

        self.x = self.point.center[0]
        self.y = self.point.center[1]

    def disconnect(self):
        self.point.figure.canvas.mpl_disconnect(self.cidpress)
        self.point.figure.canvas.mpl_disconnect(self.cidrelease)
        self.point.figure.canvas.mpl_disconnect(self.cidmotion)
