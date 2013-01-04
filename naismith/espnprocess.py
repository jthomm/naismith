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


'''
from scraping import ESPNCom, ShotChart
from bs4 import BeautifulSoup as bs

from parsing import ESPNParsedPlays

from espnprocess import MergedPlays, TimePlays

espncom = ESPNCom(bs(open('./raw-markup/400278196.html').read()))
shot_chart = ShotChart(bs(open('./raw-markup/400278196-shot.xml').read()))
espnpp = ESPNParsedPlays(espncom)

mp = MergedPlays(espnpp, shot_chart)
tp = TimePlays(mp)
'''

class MergedPlays(tuple):
    """Parsed plays merged with shot chart data.
    """

    def __new__(cls, espnpp, shot_chart):
        shots = list(shot_chart)
        lst = list()
        for play in espnpp:
            merged_play = play.copy()
            if merged_play['type'] in (u'miss', u'make', u'blocked',):
                merged_play.update(ShotLocation(shots.pop(0)).as_dict)
            lst.append(merged_play)
        return super(MergedPlays, cls).__new__(cls, lst)



class TimePlays(tuple):
    """Merged plays with period number and seconds since game began.
    """

    def __new__(cls, merged_plays):
        lst = list()
        period = 1
        for play in merged_plays:
            if play['type'] == u'period_end':
                period += 1
            elif play['type'] not in (u'game_end',):
                seconds_remaining = _clock_seconds(play['clock'])
                seconds = _seconds_since_game_began(period, seconds_remaining)
                new_play = {'period': period,
                            'seconds': seconds,}
                new_play.update(play)
                lst.append(new_play)
        return super(TimePlays, cls).__new__(cls, lst)



def _clock_seconds(clock):
    minutes, seconds = map(int, clock.split(u':'))
    return 60*minutes + seconds

def _seconds_since_game_began(current_period, seconds_remaining):
    if current_period > 4:
        # Overtime
        num_quarters_completed = 4
        num_overtimes_completed = current_period - 5
        seconds_since_current_period_began = 300 - seconds_remaining
    else:
        # Regulation
        num_quarters_completed = current_period - 1
        num_overtimes_completed = 0
        seconds_since_current_period_began = 720 - seconds_remaining
    return 720*num_quarters_completed + \
           300*num_overtimes_completed + \
           seconds_since_current_period_began



class Lineup(object):
    """Represents 5 players who are on the floor and includes methods
    for substitutions and error handling.
    """

    def __init__(self, players=None):
        if players is None:
            self.players = set()
        else:
            self.players = set(players)

    def __eq__(self, other):
        return self.players == other.players

    def remove(self, players):
        new_player_set = self.players - set(players)
        self.players = new_player_set


    def add(self, players):
        new_player_set = self.players + set(players)
        if len(new_player_set) >= 5:
            raise Exception('Adding %s to %s results in more than 5 players' % \
                            (set(players), self.players))
        else:
            self.players = new_player_set

    def substitute(player_out, player_in):
        self.remove([player_out])
        self.add([player_in])
