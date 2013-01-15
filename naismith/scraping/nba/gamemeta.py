import datetime
import re

class GameMeta(object):
    """Metadata about the game, including time and location, and 
    home and away team abbreviations.
    """

    def __init__(self, tag):
        self._tag = tag

    @property
    def _team_abbrs(self):
        return [tr.td.text for tr in \
                self._tag.find(id='nbaGITmeQtr').table.find_all('tr')]

    @property
    def _date_time_loc(self):
        """Returns a 2-element-long list with game date, time, and location:

        >>> [u'Tuesday, December 25, 2012',
        ...  u'5:30 PM ET - American Airlines Arena, Miami, FL',]
        """
        return map(_tag_text_stripped, \
                   self._tag.find(id='nbaGIStation').contents[1:])

    @property
    def _location(self):
        return self._date_time_loc[1].split(u' - ')[1]

    @property
    def away_abbr(self):
        return self._team_abbrs[0]

    @property
    def home_abbr(self):
        return self._team_abbrs[1]

    @property
    def datetime(self):
        _date_time_loc = self._date_time_loc
        _date_string = _date_time_loc[0].split(u' ', 1)[1]
        _time_string = _date_time_loc[1].split(u' - ')[0]
        return datetime.datetime.strptime(_date_string + _time_string, \
                                          u'%B %d, %Y%I:%M %p ET')

    @property
    def venue(self):
        return self._location.split(', ', 1)[0]

    @property
    def city(self):
        return self._location.split(', ', 1)[1]

    @property
    def as_dict(self):
        return {attr_name: getattr(self, attr_name) for attr_name in \
                ('away_abbr',
                 'home_abbr',
                 'datetime',
                 'venue',
                 'city',)}

"""Utils"""

def _tag_text_stripped(td):
    return re.sub(r'[\n\s]+', u' ', td.text).strip()

