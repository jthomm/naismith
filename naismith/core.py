import datetime
from bs4 import BeautifulSoup as bs
import re



class BoxScoreTrABC(object):
    """Object representation of a table row from the game's NBA.com 
    box score. This is only valid for rows which correspond to player 
    stats (i.e. not for subtotals of table headers).
    """

    def __init__(self, tds):
        self._tds = tds

    @property
    def player_url(self):
        """Returns the player's NBA.com url."""
        return unicode(self._tds[0].a.attrs['href'])

    @property
    def player_abbr(self):
        """Returns the player's abbreviated name."""
        return self._tds[0].text



class BoxScoreTr(BoxScoreTrABC):
    """Box score table row for player's that played.
    """

    @property
    def position(self):
        return self._tds[1].text

    @property
    def minutes_played(self):
        return self._tds[2].text

    @property
    def field_goals(self):
        return self._tds[3].text

    @property
    def three_pointers(self):
        return self._tds[4].text

    @property
    def free_throws(self):
        return self._tds[5].text

    @property
    def plus_minus(self):
        return int(self._tds[6].text)

    @property
    def offensive_rebounds(self):
        return int(self._tds[7].text)

    @property
    def defensive_rebounds(self):
        return int(self._tds[8].text)

    @property
    def total_rebounds(self):
        return int(self._tds[9].text)

    @property
    def assists(self):
        return int(self._tds[10].text)

    @property
    def personal_fouls(self):
        return int(self._tds[11].text)

    @property
    def steals(self):
        return int(self._tds[12].text)

    @property
    def turnovers(self):
        return int(self._tds[13].text)

    @property
    def blocked_shots(self):
        return int(self._tds[14].text)

    @property
    def points(self):
        return int(self._tds[16].text)

    @property
    def as_dict(self):
        return {attr_name: getattr(self, attr_name) for attr_name in \
                ('player_url',
                 'player_abbr',
                 'position',
                 'minutes_played',
                 'field_goals',
                 'three_pointers',
                 'free_throws',
                 'plus_minus',
                 'offensive_rebounds',
                 'defensive_rebounds',
                 'total_rebounds',
                 'assists',
                 'personal_fouls',
                 'steals',
                 'turnovers',
                 'blocked_shots',
                 'points',)}



class DNPBoxScoreTr(BoxScoreTrABC):
    """Box score table row for players that did not play.  Row will have
    two cells only.  Second cell gives reason for DNP.
    """

    @property
    def dnp_reason(self):
        return self._tds[1].text

    @property
    def as_dict(self):
        return {attr_name: getattr(self, attr_name) for attr_name in \
                ('player_url',
                 'player_abbr',
                 'dnp_reason',)}



class TeamBoxScore(tuple):
    """Object representation of a single team's box score table (box 
    score has one table for each team). Tuple contains one row for each
    player on a team's roster.
    """

    def __new__(cls, tag):
        """Must be instantiated with `tag` representing box score table."""
        lst = [box.as_dict for box in \
               [BoxScoreTr(tds) if len(tds) > 2 else DNPBoxScoreTr(tds) \
                for tds in [tr.find_all('td') \
                            for tr in tag.find_all(_is_player_tr)]]]
        return super(TeamBoxScore, cls).__new__(cls, lst)



class PlayByPlay(tuple):
    """Tuple of dictionaries containing information about each play. 
    Table rows containing only team names (two cells) are ommitted.
    """

    def __new__(cls, tag):
        """Must be instantiated with `tag` representing play-by-play table."""
        lst = list()
        for tr in tag.find_all('tr'):
            data = [_tag_text_stripped(td) for td in tr.find_all('td')]
            if len(data) == 1:
                # Usually marks the start or end of a quarter
                lst.append({'desc': data[0],
                            'clock': None,
                            'team': None,
                            'score': None,})
            elif len(data) == 3:
                # Home team plays on the right, away plays are on the left
                if data[0] == u'':
                    team = u'home'
                    desc = data[2]
                else:
                    team = u'away'
                    desc = data[0]
                try:
                    clock, score = data[1].split(u' ', 1)
                except ValueError:
                    clock = data[1]
                    score = None
                lst.append({'desc': desc,
                            'clock': clock,
                            'team': team,
                            'score': score,})
        return super(PlayByPlay, cls).__new__(cls, lst)



class GameMetaData(object):
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
        return map(_tag_text_stripped, \
                   self._tag.find(id='nbaGIStation').contents[1:])

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
        _time_string = _date_time_loc[1].split(u' - ')[0].rsplit(u' ', 1)[0]
        return datetime.datetime.strptime(_date_string + _time_string, \
                                          u'%B %d, %Y%I:%M %p')

    @property
    def location(self):
        return self._date_time_loc[1].split(u' - ')[1]



class NBACom(object):
    """Top-level API for accessing NBA.com game page data.
    """

    def __init__(self, html):
        """Initialize with html from the game's NBA.com page."""
        tag = bs(html)
        # Set metadata
        _metadata = GameMetaData(tag)
        self.away_abbr = _metadata.away_abbr
        self.home_abbr = _metadata.home_abbr
        self.datetime = _metadata.datetime
        self.location = _metadata.location
        # Set box score data
        _box_tables = tag.find_all(id='nbaGITeamStats')
        self.away_box = TeamBoxScore(_box_tables[0])
        self.home_box = TeamBoxScore(_box_tables[1])
        # Set play-by-play
        self.play_by_play = PlayByPlay(tag.find(id='nbaGIPlay').find('table'))

    @property
    def as_dict(self):
        return {attr_name: getattr(self, attr_name) for attr_name in \
                ('away_abbr',
                 'home_abbr',
                 'datetime',
                 'location',
                 'away_box',
                 'home_box',
                 'play_by_play',)}



"""Utils"""

def _tag_text_stripped(td):
    return re.sub(r'[\n\s]+', u' ', td.text).strip()

def _is_player_tr(tag):
    return tag.name == 'tr' and \
           'class' in tag.attrs and \
           tag.attrs['class'] in (['odd'], ['even']) and \
           tag.a is not None
