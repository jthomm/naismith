import datetime



PBP_URL = u'http://espn.go.com/nba/playbyplay?gameId=%s&period=0'
META_URL = u'http://espn.go.com/nba/boxscore?gameId=%s'
BOX_URL = u'http://espn.go.com/nba/boxscore?gameId=%s'
SHOT_URL = u'http://sports.espn.go.com/nba/gamepackage/data/shot?gameId=%s'
GF_URL = u'http://sports.espn.go.com/nba/gamepackage/data/gameflow?gameId=%s'



class TeamRow(object):
    """Represents one of two rows from `GameBox` instance
    """

    def __init__(self, tag):
        self._tag = tag

    @property
    def _team_links(self):
        return self._tag.ul.find_all('li')

    @property
    def _score_lis(self):
        return self._tag.find('ul', {'class': 'score'}).find_all('li')

    @property
    def url(self):
        return unicode(self._tag.p.span.a.attrs['href'])

    @property
    def nickname(self):
        return self._tag.p.span.text

    @property
    def roster_url(self):
        return unicode(self._team_links[0].a.attrs['href'])

    @property
    def stats_url(self):
        return unicode(self._team_links[1].a.attrs['href'])

    @property
    def scores(self):
        _score_lis = self._score_lis
        final_score = _score_lis.pop()
        nbsp = _score_lis.pop()
        scores = {'Final': int(final_score.text)}
        period_name = _generate_period_names()
        for li in _score_lis:
            try:
                s = int(li.text)
            except ValueError:
                # In case there are more `nbsp`s or other HTML garbage
                pass
            else:
                scores[next(period_name)] = s
        return scores

    @property
    def as_dict(self):
        return {attr_name: getattr(self, attr_name) for attr_name in \
                ('url',
                 'nickname',
                 'roster_url',
                 'stats_url',
                 'scores',)}



class GameBox(dict):
    """All metadata about a game:

    >>> from espnschedule import SchedulePage
    >>> import bs4
    >>>
    >>> tag = bs4.BeautifulSoup(open('20121226.html', 'rb').read())
    >>>
    >>> games = SchedulePage(tag)
    >>> games[1]
    {'away': {'nickname': u'Heat',
              'scores': {'Final': 105,
                         'Q1': 27,
                         'Q2': 28,
                         'Q3': 23,
                         'Q4': 27},
              'roster_url': u'http://espn.go.com/nba/team/roster/_/name/mia/miami-heat',
              'stats_url': u'http://espn.go.com/nba/team/stats/_/name/mia/miami-heat',
              'url': u'http://espn.go.com/nba/team/_/name/mia/miami-heat'},
     'home': {'nickname': u'Bobcats',
              'scores': {'Final': 92,
                         'Q1': 18,
                         'Q2': 20,
                         'Q3': 33,
                         'Q4': 21},
              'roster_url': u'http://espn.go.com/nba/team/roster/_/name/cha/charlotte-bobcats',
              'stats_url': u'http://espn.go.com/nba/team/stats/_/name/cha/charlotte-bobcats',
              'url': u'http://espn.go.com/nba/team/_/name/cha/charlotte-bobcats'},
     'espn_id': u'400278131',
     'play_by_play_url': u'http://espn.go.com/nba/playbyplay?gameId=400278131&period=0',
     'box_score_url': u'http://espn.go.com/nba/boxscore?gameId=400278131',
     'game_meta_url': u'http://espn.go.com/nba/boxscore?gameId=400278131',
     'game_flow_url': u'http://sports.espn.go.com/nba/gamepackage/data/gameflow?gameId=400278131',
     'shot_chart_url': u'http://sports.espn.go.com/nba/gamepackage/data/shot?gameId=400278131'}
    """

    def __init__(self, tag):
        dict.__init__(self)
        espn_id = unicode(tag.attrs['id'][:9])
        self['espn_id'] = espn_id
        self['play_by_play_url'] = PBP_URL % espn_id
        self['game_meta_url'] = META_URL % espn_id
        self['box_score_url'] = BOX_URL % espn_id
        self['shot_chart_url'] = SHOT_URL % espn_id
        self['game_flow_url'] =  GF_URL % espn_id
        _team_rows = map(TeamRow, tag.find_all(_is_team_row_tag))
        self['away'] = _team_rows[0].as_dict
        self['home'] = _team_rows[1].as_dict



class SchedulePage(tuple):
    """Tuple of gameboxes
    """

    def __new__(cls, tag):
        lst = list()
        game_page_date = _get_game_page_date(tag)
        for game_box_tag in tag.find_all(_is_game_box_tag):
            game_status_tag = game_box_tag.find(**{'class': 'game-status'})
            if game_status_tag.p.text[:5] == u'Final':
                game_box = GameBox(game_box_tag)
                game_box['date'] = game_page_date
                lst.append(game_box)
        return super(SchedulePage, cls).__new__(cls, lst)



def _is_game_box_tag(tag):
    return tag.attrs.get('id', '').endswith('-gamebox')

def _is_team_row_tag(tag):
    return tag.attrs.get('class', None) in (['team', 'away'], ['team', 'home'],)

def _generate_period_names():
    period_number = 1
    while True:
        if period_number <= 4:
            yield 'Q%d' % period_number
        else:
            yield 'OT%d' % (period_number - 4)
        period_number += 1

def _get_game_page_date(tag):
    _date_str = tag.find(**{'class': 'sc_logo'}).parent.find('h2').text
    return datetime.datetime.strptime(_date_str, 'Scores for %B %d, %Y').date()
