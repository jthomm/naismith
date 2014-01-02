import simplejson as json
import datetime
import re



scoreboard_path = 'http://data.sportsillustrated.cnn.com/jsonp/basketball/nba/scoreboards/2013/01/14/scoreboard.json'
playbyplay_path = 'http://data.sportsillustrated.cnn.com/jsonp/basketball/nba/gameflash/2013/01/03/32102_playbyplay.json'
box_scores_path = 'http://data.sportsillustrated.cnn.com/jsonp/basketball/nba/gameflash/2013/01/03/32102_boxscore.json'



KEY_WORDS = (
    u'jump',
    u'dunk',
    u'bank',
    u'hook',
    u'running',
    u'driving',
    u'layup',
    u'turnaround',
    u'reverse',
    u'fade away',
    u'put back',
    u'finger roll',
    u'pull up',
    u'tip',
    u'alley oop',
    u'floating',
    u'step back',
)



class Play(object):
    """Wrapper for a single play within the SI play-by-play feed
    """

    def __init__(self, data):
        """Inititialized from within the larger `PlayByPlay` container.
        """
        self._data = data

    def _player(self, i):
        i = str(i)
        last_name = self._data['player-last-name-' + i]
        if len(last_name) == 0:
            return None
        return {'last_name': unicode(last_name),
                'first_name': unicode(self._data['player-first-name-' + i]),
                'si_id': unicode(self._data['player%s-id' % i]),
                'team_abbr': unicode(
                    self._data['player-team-alias-' + i].upper()),
                'team_id': unicode(self._data['team-id-' + i]),}

    @property
    def players(self):
        return tuple(self._player(i) for i in xrange(1, 4))

    @property
    def x(self):
        data = self._data['x-coord']
        return None if len(data) == 0 else float(data)

    @property
    def y(self):
        data = self._data['y-coord']
        return None if len(data) == 0 else float(data)

    @property
    def distance(self):
        data = self._data['distance']
        return None if len(data) == 0 else float(data)

    @property
    def player_score(self):
        return int(self._data['player-score'])

    @property
    def detail_desc(self):
        return unicode(self._data['detail-desc'])

    @property
    def detail_id(self):
        return unicode(self._data['detail-id'])

    @property
    def details(self):
        return unicode(self._data['details'])

    @property
    def event_desc(self):
        return unicode(self._data['event-desc'])

    @property
    def event_id(self):
        return unicode(self._data['event-id'])

    @property
    def point_value(self):
        data = self._data['points-type']
        return None if len(data) == 0 else int(data)

    @property
    def is_fastbreak(self):
        data = self._data['fastbreak']
        return None if data == '' else data

    @property
    def is_in_paint(self):
        data = self._data['in-paint']
        return None if data == '' else data

    @property
    def is_second_chance(self):
        data = self._data['second-chance']
        return None if data == '' else data

    @property
    def is_off_turnover(self):
        data = self._data['off-turnover']
        return None if data == '' else data

    @property
    def player_score(self):
        return int(self._data['player-score'])

    @property
    def player_fouls(self):
        return int(self._data['player-fouls'])

    @property
    def away_score(self):
        return int(self._data['visitor-score'])

    @property
    def home_score(self):
        return int(self._data['home-score'])

    @property
    def away_fouls(self):
        return int(self._data['visitor-fouls'])

    @property
    def home_fouls(self):
        return int(self._data['home-fouls'])

    @property
    def quarter(self):
        return int(self._data['quarter'])

    @property
    def minutes(self):
        return int(self._data['time-minutes'])

    @property
    def seconds(self):
        return int(self._data['time-seconds'])

    @property
    def tags(self):
        return tuple(kw for kw in KEY_WORDS if kw in self.detail_desc.lower())

    @property
    def as_dict(self):
        return {attr_name: getattr(self, attr_name) for attr_name in \
                ('players',
                 'x',
                 'y',
                 'distance',
                 'player_score',
                 'detail_desc',
                 'detail_id',
                 'details',
                 'event_desc',
                 'event_id',
                 'point_value',
                 'is_fastbreak',
                 'is_in_paint',
                 'is_second_chance',
                 'is_off_turnover',
                 'player_score',
                 'player_fouls',
                 'away_score',
                 'home_score',
                 'away_fouls',
                 'home_fouls',
                 'quarter',
                 'minutes',
                 'seconds',
                 'tags',)}



class SICom(object):
    """Container for SI play-by-play feed
    """

    def __init__(self, response_string):
        """Initialize using response string from getting SI's json feed:

        >>> import requests
        >>> url = 'http://data.sportsillustrated.cnn.com/jsonp/basketball/nba/gameflash/2013/01/03/32102_playbyplay.json'
        >>> response_string = response.get(url).text

        JSON data will almost certainly be wrapped with 'callbackWrapper(' 
        on the left and ');' on the right.
        """
        mo = re.search(r'callbackWrapper\((.+?)\);$', response_string)
        game_json = response_string if mo is None else mo.groups(0)[0]
        self._data = json.loads(game_json)

    @property
    def si_id(self):
        return self._data['playbyplay']['contest']['id']

    @property
    def datetime(self):
        game_date = self._data['playbyplay']['meta']['game-date']
        datetime_str = u' '.join([game_date['url'], game_date['game-time']])
        return datetime.datetime.strptime(datetime_str, '%Y/%m/%d %I:%M %p ET')

    @property
    def venue(self):
        return self._data['playbyplay']['contest']['venue']

    @property
    def city(self):
        return self._data['playbyplay']['contest']['venue-city']

    @property
    def state(self):
        return self._data['playbyplay']['contest']['venue-state']

    @property
    def away(self):
        team = self._data['playbyplay']['contest']['team']
        raw_team_data = team[1] if team[1]['side'] == 'visiting' else team[0]
        return {'nickname': raw_team_data['name'],
                'location': raw_team_data['city'],
                'abbr': raw_team_data['three-letter-abbr'],
                'stats_inc_id': raw_team_data['id'],}

    @property
    def home(self):
        team = self._data['playbyplay']['contest']['team']
        raw_team_data = team[0] if team[0]['side'] == 'home' else team[1]
        return {'nickname': raw_team_data['name'],
                'location': raw_team_data['city'],
                'abbr': raw_team_data['three-letter-abbr'],
                'stats_inc_id': raw_team_data['id'],}

    @property
    def plays(self):
        return tuple(Play(d).as_dict for d in self._data['playbyplay']['plays']['play'])

    @property
    def as_dict(self):
        return {attr_name: getattr(self, attr_name) for attr_name in \
                ('si_id',
                 'datetime',
                 'venue',
                 'city',
                 'state',
                 'away',
                 'home',
                 'plays',)}



