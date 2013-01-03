from math import atan2

class ShotLocation(object):
    """Convert absolute `x` and `y` coordinates from `shot_chart_entry`
    into cartesian and polar coordinates, relative to center of shooting team's
    hoop.
    """

    def __init__(self, shot_chart_entry):
        self.team = shot_chart_entry['team']
        self.absolute_x = shot_chart_entry['x']
        self.absolute_y = shot_chart_entry['y']

    @property
    def x(self):
        if self['team'] == u'away':
            return self.absolute_x - 25
        else:
            return 25 - self.absolute_x

    @property
    def y(self):
        if self['team'] == u'away':
            return self.absolute_y - 5.25
        else:
            return 88.75 - self.absolute_y

    @property
    def r(self):
        return (self.x**2.0 + self.y**2.0)**0.5

    @property
    def theta(self):
        return atan2(self.x, self.y)

    @property
    def as_dict(self):
        return {'absolute_x': self.absolute_x,
                'absolute_y': self.absolute_x,
                'x': self.x,
                'y': self.y,
                'r': self.r,
                'theta': self.theta,}
