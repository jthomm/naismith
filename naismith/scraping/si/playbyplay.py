import simplejson as json
import datetime
import re



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

def _get_player(data, i):
    i = str(i)
    last_name = data['player-last-name-' + i]
    return None if last_name == '' else {
        'last_name': unicode(last_name),
        'first_name': unicode(data['player-first-name-' + i]),
        'si_id': unicode(data['player%s-id' % i]),
        'team_abbr': unicode(data['player-team-alias-' + i].upper()),
        'team_id': unicode(data['team-id-' + i]),
    }



class Play(object):
    """Wrapper for a single play within the SI play-by-play feed
    """

    def __init__(self, data):
        """Inititialized from within the larger `PlayByPlay` container.
        """
        self._data = data

    def _player(self, i):
        return _get_player(self._data, i)
        #i = str(i)
        #last_name = self._data['player-last-name-' + i]
        #if len(last_name) == 0:
        #    return None
        #return {'last_name': unicode(last_name),
        #        'first_name': unicode(self._data['player-first-name-' + i]),
        #        'si_id': unicode(self._data['player%s-id' % i]),
        #        'team_abbr': unicode(
        #            self._data['player-team-alias-' + i].upper()),
        #        'team_id': unicode(self._data['team-id-' + i]),}

    @property
    def players(self):
        return tuple(self._player(i) for i in xrange(1, 4))

    @property
    def game_id(self):
        return unicode(self._data['game_id'])

    @property
    def away_abbr(self):
        return unicode(self._data['away_abbr'])

    @property
    def home_abbr(self):
        return unicode(self._data['home_abbr'])

    @property
    def x(self):
        """Positive values are right of the hoop (when standing behind it)
        for the home team and left for the away team.
        """
        is_away = self.players[0] is not None and \
                  self.players[0]['team_abbr'] == self.away_abbr
        transform = -1 if is_away else 1
        data = self._data['x-coord']
        return None if len(data) == 0 else transform*float(data)

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
        """Non-None for field goals, free throws, and fouls
        """
        data = self._data['fastbreak']
        return None if len(data) == 0 else True if data == 'true' else False

    @property
    def is_in_paint(self):
        """Non-None for field goals
        """
        data = self._data['in-paint']
        return None if len(data) == 0 else True if data == 'true' else False

    @property
    def is_second_chance(self):
        """Non-None for *some* field goals and *some* free throws. The same 
        set of plays for which `is_off_turnover` is not None.
        """
        data = self._data['second-chance']
        return None if len(data) == 0 else True if data == 'true' else False

    @property
    def is_off_turnover(self):
        """Non-None for *some* field goals and *some* free throws. The same
        set of plays for which `is_second_chance` is not None.
        """
        data = self._data['off-turnover']
        return None if len(data) == 0 else True if data == 'true' else False

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
        return float(self._data['time-seconds'])

    @property
    def tags(self):
        return tuple(kw for kw in KEY_WORDS if kw in self.detail_desc.lower()) \
               if self.event_id in ('3', '4',) else None

    @property
    def as_dict(self):
        return {attr_name: getattr(self, attr_name) for attr_name in \
                ('players',
                 'game_id',
                 'away_abbr',
                 'home_abbr',
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



class PlayByPlay(object):
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
        return unicode(self._data['playbyplay']['contest']['id'])

    @property
    def datetime(self):
        game_date = self._data['playbyplay']['meta']['game-date']
        datetime_str = u' '.join([game_date['url'], game_date['game-time']])
        strptime_fmt = '%Y/%m/%d %I:%M %p ET'
        try:
            return datetime.datetime.strptime(datetime_str, strptime_fmt)
        except ValueError:
            print 'There was an issue converting {0}'.format(datetime_str)
            return datetime.datetime.strptime(datetime_str[:10] + ' 12:00 PM ET',
                                              strptime_fmt)
            print 'Used {0} instead'.format(datetime_str[:10] + ' 12:00 PM ET')

    @property
    def venue(self):
        return unicode(self._data['playbyplay']['contest']['venue'])

    @property
    def city(self):
        return unicode(self._data['playbyplay']['contest']['venue-city'])

    @property
    def state(self):
        return unicode(self._data['playbyplay']['contest']['venue-state'])

    def _get_team(self, side):
        teams = self._data['playbyplay']['contest']['team']
        team = teams[0] if teams[0]['side'] == side else teams[1]
        return {'nickname': unicode(team['name']),
                'location': unicode(team['city']),
                'abbr': unicode(team['three-letter-abbr'].upper()),
                'stats_inc_id': unicode(team['id']),}

    @property
    def away(self):
        return self._get_team('visiting')

    @property
    def home(self):
        return self._get_team('home')

    @property
    def game_id(self):
        return u'-'.join([self.datetime.strftime('%Y%m%d'),
                          self.away['abbr'],
                          self.home['abbr'],])

    @property
    def plays(self):
        plays = list()
        for data in self._data['playbyplay']['plays']['play']:
            data['game_id'] = self.game_id
            data['away_abbr'] = self.away['abbr']
            data['home_abbr'] = self.home['abbr']
            plays.append(Play(data).as_dict)
        return plays

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
                 'game_id',
                 'plays',)}
