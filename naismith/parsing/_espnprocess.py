from espnparse import Parser
from itertools import ifilter
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
        if self.team == u'away':
            return self.absolute_x - 25
        else:
            return 25 - self.absolute_x

    @property
    def y(self):
        if self.team == u'away':
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
                'absolute_y': self.absolute_y,
                'x': self.x,
                'y': self.y,
                'r': self.r,
                'theta': self.theta,}



class ParsedPlay(dict):
    """Dictionary containing basic information about a play or event 
    parsed from its description.
    """

    def __init__(self, parser, scraped_play):
        dict.__init__(self)
        self.update(scraped_play)
        self.update(parser.resolve_play_type(scraped_play['desc']))



class ParsedShot(dict):
    """`ParsedPlay` dictionary containing additional information about 
    shot location.
    """

    def __init__(self, parsed_play, shot_chart_entry):
        dict.__init__(self)
        self.update(parsed_play)
        if self['type'] not in (u'make', u'miss', u'blocked',):
            raise TypeError('%s is not a shot: ' % self)
        else:
            self['shot_location'] = ShotLocation(shot_chart_entry).as_dict



class MergedPlays(tuple):
    """Tuple of dictionaries containing information scraped from ESPN 
    shot chart and play-by-play, as well as information parsed from play-by-play 
    event descriptions.
    """

    def __new__(cls, espncom, shot_chart):
        # Parse play descriptions
        parser = Parser()
        lst = list()
        for scraped_play in espncom['plays']:
            parsed_play = ParsedPlay(parser, scraped_play)
            if parsed_play['type'] in (u'make', u'miss', u'blocked',):
                shot = Shot(parsed_play, shot_chart.pop(0))
                lst.append(shot)
            else:
                lst.append(parsed_play)
        return super(Plays, cls).__new__(cls, lst)
