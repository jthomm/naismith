import simplejson as json
import datetime
import re



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
        self._raw_data = json.loads(game_json)

    @property
    def si_id(self):
        return self._raw_data['playbyplay']['contest']['id']

    @property
    def datetime(self):
        game_date = self._raw_data['playbyplay']['meta']['game-date']
        datetime_str = u' '.join([game_date['url'], game_date['game-time']])
        return datetime.datetime.strptime(datetime_str, '%Y/%m/%d %I:%M %p ET')

    @property
    def venue(self):
        return self._raw_data['playbyplay']['contest']['venue']

    @property
    def city(self):
        return self._raw_data['playbyplay']['contest']['venue-city']

    @property
    def state(self):
        return self._raw_data['playbyplay']['contest']['venue-state']

    @property
    def away(self):
        team = self._raw_data['playbyplay']['contest']['team']
        raw_team_data = team[1] if team[1]['side'] == 'visiting' else team[0]
        return {'nickname': raw_team_data['name'],
                'location': raw_team_data['city'],
                'abbr': raw_team_data['three-letter-abbr'],
                'stats_inc_id': raw_team_data['id'],}

    @property
    def home(self):
        team = self._raw_data['playbyplay']['contest']['team']
        raw_team_data = team[0] if team[0]['side'] == 'home' else team[1]
        return {'nickname': raw_team_data['name'],
                'location': raw_team_data['city'],
                'abbr': raw_team_data['three-letter-abbr'],
                'stats_inc_id': raw_team_data['id'],}

    @property
    def plays(self):
        return tuple(self._raw_data['playbyplay']['plays']['play'])

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
