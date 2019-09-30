from matplotlib.lines import Line2D


class DraggableLine(Line2D):
    def __init__(self, parent, index, point_a, point_b, linewidth=None, linestyle=None, color=None, marker=None,
                 markersize=None, markeredgewidth=None, markeredgecolor=None, markerfacecolor=None,
                 markerfacecoloralt='none', fillstyle=None, antialiased=None, dash_capstyle=None, solid_capstyle=None,
                 dash_joinstyle=None, solid_joinstyle=None, pickradius=5, drawstyle=None, markevery=None, **kwargs):
        self.parent = parent
        self.index = index
        self.end_a = point_a
        self.end_b = point_b

        line_x = [self.end_a.x, self.end_b.x]
        line_y = [self.end_a.y, self.end_b.y]

        super().__init__(line_x, line_y, linewidth, linestyle, color, marker, markersize,
                      markeredgewidth, markeredgecolor, markerfacecolor, markerfacecoloralt,
                      fillstyle, antialiased, dash_capstyle, solid_capstyle, dash_joinstyle,
                      solid_joinstyle, pickradius, drawstyle, markevery, **kwargs)
