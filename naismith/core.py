mport datetime
from bs4 import BeautifulSoup as bs
import re

class PlayerTr(object):

    def __init__(self, soup):
        self._soup = soup
        self._tds = soup.find_all('td')

    @property
    def url(self):
        return unicode(self._tds[0].a.attrs['href'])

    @property
    def abbr(self):
        return self._tds[0].text

    @property
    def pos(self):
        return self._tds[1].text

    @property
    def seconds(self):
        minutes, seconds = map(int, self._tds[2].text.split(u':'))
        return 60*minutes + seconds

    @property
    def all_fg(self):
        made, attempted = map(int, self._tds[3].text.split(u'-'))
        return dict(m=made, a=attempted)

    @property
    def three_fg(self):
        made, attempted = map(int, self._tds[4].text.split(u'-'))
        return dict(m=made, a=attempted)

    @property
    def free_throws(self):
        made, attempted = map(int, self._tds[5].text.split(u'-'))
        return dict(m=made, a=attempted)

    @property
    def plus_minus(self):
        return int(self._tds[6].text)

    @property
    def off_rebounds(self):
        return int(self._tds[7].text)

    @property
    def def_rebounds(self):
        return int(self._tds[8].text)

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
    def blocks(self):
        return int(self._tds[14].text)

    @property
    def points(self):
        return int(self._tds[16].text)

    @property
    def as_dict(self):
        try:
            return {'url': self.url,
                    'abbr': self.abbr,
                    'pos': self.pos,
                    'seconds': self.seconds,
                    'all_fg': self.all_fg,
                    'three_fg': self.three_fg,
                    'free_throws': self.free_throws,
                    'plus_minus': self.plus_minus,
                    'off_rebounds': self.off_rebounds,
                    'def_rebounds': self.def_rebounds,
                    'assists': self.assists,
                    'personal_fouls': self.personal_fouls,
                    'steals': self.steals,
                    'turnovers': self.turnovers,
                    'blocks': self.blocks,
                    'points': self.points,}
        except IndexError:
            return {'url': self.url,
                    'abbr': self.abbr,
                    'absence': self._tds[1].text,}


class TeamStats(object):

    def __init__(self, soup):
        _team_and_record = soup.find('thead').text
        self.team = _team_and_record[:_team_and_record.index('(')-1]
        self.players = [PlayerTr(tr).as_dict for tr in \
                        soup.find_all(_is_player_tr)]


class GameInfo(object):

    def __init__(self, soup):
        self._soup = soup
        _abbrs = [tr.td.text for tr in self._score_table.find_all('tr')]
        self.away_abbr = _abbrs[0]
        self.home_abbr = _abbrs[1]
        self.location = self._time_and_location.split(u' - ')[1]
        _dt_string = u'%s %s' % (self._date_string, self._time_string)
        _fmt_string = u'%B %d, %Y %I:%M %p'
        self.datetime = datetime.datetime.strptime(_dt_string, _fmt_string)

    @property
    def _score_table(self):
        return self._soup.find(id='nbaGITmeQtr').find('table')

    @property
    def _date_location_div(self):
        return self._soup.find(id='nbaGIStation')

    @property
    def _date_string(self):
        _date_string = self._date_location_div.contents[1].text
        return _date_string[_date_string.index(',')+2:]

    @property
    def _time_and_location(self):
        return _tag_text(self._date_location_div.contents[2])

    @property
    def _time_string(self):
        _time_string = self._time_and_location.split(u' - ')[0]
        return _time_string[:_time_string.index('M')+1]

    @property
    def as_dict(self):
        return {'datetime': self.datetime,
                'location': self.location,
                'away_abbr': self.away_abbr,
                'home_abbr': self.home_abbr,}


class PBP(tuple):

    def __new__(cls, table):
        lst = list()
        for tr in table.find_all('tr'):
            row = _tr_text(tr)
            if len(row) == 1:
                lst.append({'desc': row[0],
                            'clock': None,
                            'team': None,
                            'score': None,})
            elif len(row) == 3:
                if row[0] == u'':
                    team = u'home'
                    desc = row[2]
                else:
                    team = u'away'
                    desc = row[0]
                try:
                    clock, score = row[1].split(u' ', 1)
                except ValueError:
                    clock = row[1]
                    score = None
                lst.append({'desc': desc,
                            'clock': clock,
                            'team': team,
                            'score': score,})
        return super(PBP, cls).__new__(cls, lst)

class NBACom(object):

    def __init__(self, html):
        # Cache soup from html
        self._soup = bs(html)
        # Set game info
        _game_info = GameInfo(self._soup)
        self.location = _game_info.location
        self.datetime = _game_info.datetime
        self.away_abbr = _game_info.away_abbr
        self.home_abbr = _game_info.home_abbr
        # Set players
        _team_stats = map(TeamStats, self._team_tables)
        self.away_team = _team_stats[0].team
        self.home_team = _team_stats[1].team
        self.away_players = _team_stats[0].players
        self.home_players = _team_stats[1].players
        # Set pbp
        self.pbp = PBP(self._pbp_table)

    @property
    def _team_tables(self):
        return self._soup.find_all(id='nbaGITeamStats')

    @property
    def _pbp_table(self):
        return self._soup.find(id='nbaGIPlay').find('table')

    @property
    def game_id(self):
        return u''.join((self.datetime.strftime('%Y%m%d'),
                         self.away_abbr, self.home_abbr,))

    @property
    def as_dict(self):
        return {'game_id': self.game_id,
                'location': self.location,
                'datetime': self.datetime,
                'away_abbr': self.away_abbr,
                'home_abbr': self.home_abbr,
                'away_team': self.away_team,
                'home_team': self.home_team,
                'away_players': self.away_players,
                'home_players': self.home_players,
                'play_by_play': self.pbp,}



def _tag_text(td):
    return re.sub(r'[\n\s]+', u' ', td.text).strip()

def _tr_text(tr):
    return [_tag_text(td) for td in tr.find_all('td')]

def _is_player_tr(tag):
    return tag.name == 'tr' and \
           'class' in tag.attrs and \
           tag.attrs['class'] in (['odd'], ['even']) and \
           tag.a is not None
