import re



class TeamDiv(object):
    """Team info
    """

    def __init__(self, tag):
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
    """Game metadata
    """

    def __init__(self, tag):
        self._tag = tag

    @property
    def url(self):
        return u'http://www.nba.com%s' % self._tag.a.attrs['href']

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
                'nba_id': self.nba_id,
                'away': self.away,
                'home': self.home,}



class SchedulePage(tuple):
    """Tuple of `GameLine` dictionaries
    """

    def __new__(cls, tag):
        lst = [GameLine(game_line_tag).as_dict for game_line_tag in \
               tag.find_all('div', {'class': 'Recap GameLine'})]
        return super(SchedulePage, cls).__new__(cls, lst)

    def display_options(self):
        for i, game_line in enumerate(self):
            index_str = (u'%d.' % i).ljust(3)
            away_str = (u'%s (%d)' % (game_line['away']['team_abbr'],
                                      game_line['away']['final_score'],)).ljust(9)
            home_str = (u'%s (%d)' % (game_line['home']['team_abbr'],
                                      game_line['home']['final_score'],)).ljust(10)
            print u'%s %s @ %s' % (index_str, away_str, home_str,)
