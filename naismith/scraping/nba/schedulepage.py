import re



class TeamDiv(object):
    """`div` containing information about a single team in a single game.  
    Each "game line" `div` contains two of these, one for the away team and 
    another for the home team.
    """

    def __init__(self, tag):
        """Initialize with `tag` representing a single team `div`:

        >>> tag = game_line_tag.find(**{'class': 'nbaModTopTeamAw'})
        >>> away = TeamDiv(tag)
        """
        self._tag = tag

    @property
    def team_abbr(self):
        return self._tag.find(**{'class': 'nbaModTopTeamName'}).text.upper()

    @property
    def final_score(self):
        return int(self._tag.find(**{'class': 'nbaModTopTeamNum'}).text)

    @property
    def as_dict(self):
        return {'team_abbr': self.team_abbr,
                'final_score': self.final_score,}



class GameLine(object):
    """`div` containing information about a single game.  NBA.com schedule 
    page has one "game line" per game.
    """

    def __init__(self, tag):
        """Initialize with `tag` representing a single "game line" `div`:

        >>> game_line_tags = tag.find_all('div', {'class': 'Recap GameLine'})
        >>> gl = GameLine(game_line_tags[0])
        """
        self._tag = tag

    @property
    def url(self):
        return u'http://www.nba.com%s' % self._tag.a.attrs['href']

    @property
    def time(self):
        return self._tag.find(**{'class': 'nbaFnlStatTxSm'}).text.upper()

    @property
    def nba_id(self):
        match = re.search(r'(\d{8})/(\w{6})', self.url)
        return u''.join(match.groups())

    @property
    def away(self):
        return TeamDiv(self._tag.find(**{'class': 'nbaModTopTeamAw'})).as_dict

    @property
    def home(self):
        return TeamDiv(self._tag.find(**{'class': 'nbaModTopTeamHm'})).as_dict

    @property
    def as_dict(self):
        return {'url': self.url,
                'time': self.time,
                'nba_id': self.nba_id,
                'away': self.away,
                'home': self.home,}



class SchedulePage(tuple):
    """Tuple of all `GameLine` objects (as dictionaries) generated from a 
    single date's worth of games.
    """

    def __new__(cls, tag):
        """Instantiate with `tag` representing entire NBA.com schedule page:

        >>> import requests
        >>> import bs4
        >>> 
        >>> html = requests.get('http://www.nba.com/gameline/20130115/').text
        >>> tag = bs4.BeautifulSoup(tag)
        >>> schedule_page = SchedulePage(tag)
        """
        lst = [GameLine(game_line_tag).as_dict for game_line_tag in \
               tag.find_all('div', {'class': 'Recap GameLine'})]
        return super(SchedulePage, cls).__new__(cls, lst)
